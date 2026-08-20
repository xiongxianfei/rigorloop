# Bugfix Skill Simplification Contract

## Owning change record

`docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-20-bugfix-skill-simplification.md`

## Goal and context

The published `bugfix` skill remains a single compact `SKILL.md`, but its behavior becomes a closed support-stage contract. The contract separates requested operation, command authority, repository-write authority, evidence quality, proof authoring, production correction, validation, owner routing, terminal result, and downstream handoff. It preserves explicit-step bugfix behavior and forbids speculative correction, cross-owner lifecycle mutation, or unsupported completion claims.

## Glossary

| Term | Meaning |
| --- | --- |
| Concrete defect | One normalized unexpected behavior in one repository with an identifiable expected-versus-actual outcome. |
| Proof authoring | A bounded pre-correction phase that may create tests, fixtures, test-only helpers, or controlled reproduction artifacts, but may not change production behavior. |
| Production correction | The smallest authorized production change that restores one settled behavior basis. |
| Deterministic alternative | An independently repeatable command, fixture, static contract check, or controlled manual procedure with exact inputs, environment, steps, expected observation, and completion condition. |
| Resolvable restoration | Restoration to one exact current authoritative behavior basis with no equal- or higher-priority conflict and no new or reinterpreted observable behavior. |
| Proof identity | The bound command or procedure, fixtures, inputs, environment assumptions, and expected pre-fix observation reused unchanged after correction. |

## Examples first

Example E1: explicit diagnosis stays read-only
Given a concrete defect and an invocation that says `$bugfix diagnose the root cause`
When the skill classifies the request
Then it selects `diagnose-only`, may run only bounded commands, and intentionally writes no tracked file or external state.

Example E2: a bare bugfix request is narrowly writable
Given one concrete defect in one repository and no narrower requested outcome
When `$bugfix` is invoked
Then it selects `fix` and establishes portable request-bound authority only for that defect and the exact permitted write categories.

Example E3: proof is authored before production
Given a reproduced implementation defect, settled behavior basis, supported cause, feasible automated testing, and no failing regression test
When the fix proceeds
Then only the bounded automated proof is authored and production mutation remains blocked until that proof fails for the defect.

Example E4: infeasibility is not proof
Given automated testing is `infeasible-with-rationale` but no deterministic alternative exists
When production correction is considered
Then the action is `stop-blocked` and no production behavior changes.

Example E5: contract gaps route upstream
Given the expected outcome is missing, conflicting, or a behavior-change request
When the cause is evaluated
Then the skill routes to `spec` or the exact contract owner and performs no bugfix product mutation.

Example E6: proof identity cannot drift
Given a failing proof was recorded before correction
When the test, fixture, command, input, or environment changes before the post-fix run
Then the changed proof cannot establish that the original regression now passes.

Example E7: unknown cause is truthful but not fixable
Given reproduction exists but root cause remains `unknown`
When the invocation returns
Then it reports `diagnosis-incomplete` or routes to an owner and never reports `fix-applied`.

Example E8: governed signals fail closed
Given two conflicting change IDs or an escaped governed path
When the skill classifies context
Then it stops without portable fallback and does not mutate lifecycle state.

Example E9: completed correction wins over broader phase eligibility
Given a correction exists and all identity-equal proof and blast-radius checks pass
When current action is selected
Then `complete-fix` is selected before any broader proof or correction row.

Example E10: implementation hands off only to code review
Given production code changed and local proof passed
When the invocation completes
Then the result is `fix-applied`, the immediate next stage is `code-review`, and no later gate starts automatically.

## Requirements

R1. The published package MUST contain exactly one `skills/bugfix/SKILL.md` and MUST add no reference, asset, script, template, or executable runtime for this change.

R2. The skill MUST classify operation as exactly `diagnose-only` or `fix`; an invocation without one concrete defect MUST return `blocked` without mutation.

R3. Explicit diagnosis, explanation, reproduction, or root-cause wording MUST select `diagnose-only` even when `$bugfix` is named. Explicit repair wording or bare `$bugfix` with one concrete defect and no narrower outcome MUST select `fix`. Conflicting diagnosis and repair wording MUST permit diagnosis only and block mutation pending an explicit outcome.

R4. Command authority MUST be exactly `not-required`, `current-bounded`, `absent-or-stale`, or `invalid-or-ambiguous`. Repository-write authority MUST be exactly `none`, `portable-request-bound`, `governed-scope-bound`, `absent-or-stale`, or `invalid-or-ambiguous`.

R5. Every writable fix MUST bind repository identity, normalized defect target, authority source, allowed path roots, allowed write categories, permitted command set or command owner, governing contract identity, and current evidence identities. A diagnosis-to-fix expansion MUST rerun this preflight.

R6. Diagnose-only MAY run exact inspection or reproduction commands only under current bounded authority and MUST intentionally change no tracked file or durable external state. Unknown, destructive, privileged, network, database, or durable external effects require their existing separate authority or MUST be skipped. Unexpected mutation MUST stop and be reported.

R7. The skill MUST classify reproduction, contract basis, test feasibility, regression proof, and root-cause support using only the closed values selected by the approved proposal. Unknown values MUST fail closed before consistency checks.

R8. `resolvable-restoration` MUST bind one exact current authoritative source, owner, precedence, affected behavior, expected result, and conflict check. It MUST NOT add, remove, broaden, narrow, or reinterpret observable behavior.

R9. A deterministic alternative MUST record its exact procedure, inputs, environment assumptions, expected observation, objective completion condition, and limitations. Subjective inspection and infeasibility alone MUST NOT count as proof.

R10. The execution phases MUST be ordered `diagnosis`, `proof-authoring`, `production-correction`, and `post-fix-validation`. Proof-authoring and production correction MUST use separate eligibility gates.

R11. After all non-proof prerequisites pass, proof authoring MAY write only bounded tests, fixtures, test-only helpers, or controlled reproduction artifacts. Production behavior MUST remain unchanged until a failing automated proof exists or a complete deterministic alternative exists with `infeasible-with-rationale`.

R12. The proof-action matrix MUST be exhaustive and pairwise non-overlapping. `failing-automated-test` permits correction; conflicting proof blocks; feasible missing or alternative-only proof selects automated proof authoring; unresolved feasibility selects feasibility resolution; infeasible complete alternative permits correction; infeasible missing proof blocks.

R13. Before production correction, the skill MUST record one proof identity. Post-fix validation MUST rerun that identity unchanged and record the post-fix observation. Changed proof components MUST create a different proof and MUST NOT be reported as the original proof passing.

R14. Root cause MUST use exactly `implementation-defect`, `contract-gap`, `integration-mismatch`, `data-or-migration`, `race-or-timing`, `configuration-or-environment`, `test-defect`, `external-dependency`, or `unknown`.

R15. Current action MUST use exactly `stop-blocked`, `route-owner`, `continue-diagnosis`, `complete-diagnosis`, `resolve-test-feasibility`, `author-automated-proof`, `apply-production-correction`, `run-post-fix-validation`, or `complete-fix`. Terminal result MUST use exactly `diagnosis-complete`, `diagnosis-incomplete`, `fix-applied`, `routed-to-owner`, or `blocked`.

R16. Action selection MUST evaluate specific blockers and completed correction states before broader phase eligibility. Every recognized state combination MUST select exactly one reachable action. Every returning invocation MUST derive exactly one terminal result, and intermediate actions MUST NOT be emitted as terminal results.

R17. Cause `unknown` MUST NOT authorize production mutation. Cause `contract-gap` and basis `missing`, `conflicting`, or `behavior-change-request` MUST route to the exact contract owner. A new long-lived design decision MUST route to `architecture`.

R18. A `test-defect` correction MUST have a `settled` or `resolvable-restoration` basis and MUST NOT weaken expectations speculatively. Configuration, environment, or external-dependency causes MAY enter correction only when a settled product basis and current scope require a bounded resilience change; otherwise they route to the actual owner.

R19. Independent defects MUST be decomposed unless evidence establishes one shared root cause, behavior basis, correction scope, and proof bundle.

R20. Governed-signal classification MUST be exactly `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. Any explicit or structured governed signal counts even when invalid. Invalid, stale, conflicting, duplicated, or escaped signals MUST stop without portable fallback.

R21. Portable and governed diagnose-only operations MUST write nothing. Portable and governed proof and correction writes MUST remain within the exact authorized table in the approved proposal. Proposal, spec, architecture, ADR, plan, change metadata, workflow, automation, review, review-resolution, explanation, verify, PR, release, and publication surfaces MUST remain read-only to bugfix.

R22. When governed durable evidence is required, the skill MUST use one exact existing authorized bugfix evidence destination. Missing or ambiguous placement MUST block durable recording and MUST NOT create a path, artifact entry, or lifecycle state.

R23. Completion MUST rerun the original reproduction or deterministic alternative, the identity-equal regression proof, and the smallest surrounding validation justified by blast radius. A failed, conflicting, skipped-required, or identity-mismatched check MUST prevent `fix-applied`.

R24. The result MUST report operation, terminal result, authority classifications, repository and defect scope, commands actually run, proof identity, unexecuted checks, uncertainty, changed surfaces, and next owner. Changed implementation MUST route immediately to independent `code-review`; no downstream stage starts automatically.

R25. Bugfix MUST NOT claim code-review approval, explain-change completion, verification, hosted CI, branch readiness, PR readiness, release, deployment, publication, lifecycle completion, or `Done`.

R26. The implementation MUST preserve every behaviorally meaningful legacy rule or record an approved disposition, preserve parser- or documentation-sensitive literals, validate all existing package projections, and reduce both LF-normalized Unicode whitespace-separated words and UTF-8 bytes for the root and complete package.

R27. Acceptance MUST use deterministic repository-owned static scenarios and ordinary lifecycle reviews. It MUST NOT execute a live repair task, target agent, external issue or incident system, or introduce a persistent bug transaction.

## Inputs and outputs

Inputs are one concrete defect, request wording, repository identity, governing behavior evidence, current code and tests, command authority, write authority, governed signals when present, reproduction evidence, and project-owned validation commands. Outputs are a bounded diagnostic or fix result, exact local changes when authorized, proof and command evidence, uncertainty, changed surfaces, next owner, and no lifecycle mutation.

## State and invariants

- Operation, command authority, write authority, evidence axes, root cause, current action, and terminal result are independently classified.
- Unknown values fail before dependent consistency logic.
- Diagnosis never intentionally mutates tracked or external state.
- Proof-authoring never changes production behavior.
- Production correction never precedes exact regression proof.
- Post-fix success never changes the pre-fix proof identity.
- Upstream and lifecycle owners remain authoritative and read-only.
- A returning invocation has exactly one terminal result.
- Direct and manual bugfix invocations remain isolated and explicit-step.

## Error and boundary behavior

Unknown, missing, stale, conflicting, escaped, duplicated, unsafe, or ambiguous identity, authority, contract, proof, or governed context fails closed at the earliest dependent boundary. A blocked operation preserves evidence already obtained but performs no unauthorized correction, lifecycle mutation, or downstream continuation.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R2, R3, R7, R14, R15 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R10, R11, R12, R13, R16, R23 | BND-STATE-001 | - |
| identity-authority | applicable | R4, R5, R6, R8, R20, R21, R22 | BND-AUTH-001 | - |
| composition-path | applicable | R17, R18, R19, R21, R24 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R5, R13, R16, R23 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R6, R9, R12, R16, R22, R23 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R1, R21, R26 | BND-COMPAT-001 | - |
| external-environment | applicable | R6, R9, R18, R27 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R2, R3, R7, R14, R15 | concrete or absent defect; diagnosis, fix, or conflicting wording; recognized or unknown closed value | One concrete defect and recognized values are required before dependent action | Valid inputs select one operation and action; absent or unknown input blocks | R2 |
| BND-STATE-001 | state-lifecycle | R10, R11, R12, R13, R16, R23 | diagnosis → proof authoring → correction → validation → completion; illegal skips | Each phase satisfies its own gate and completion rows precede broader eligibility | Legal progress continues; illegal or failed transitions block; passed validation completes | R10 |
| BND-AUTH-001 | identity-authority | R4, R5, R6, R8, R20, R21, R22 | absent, current, stale, conflicting, ambiguous, portable, governed | Commands and writes remain exact, current, and owner-scoped; invalid governed signals never fall back | Current bounded authority permits only its surface; all other states block | R5 |
| BND-COMPOSE-001 | composition-path | R17, R18, R19, R21, R24 | bugfix-owned proof/correction, contract owner, architecture owner, system owner, code-review handoff | Bugfix never substitutes for another owner or combines independent defects | Writable causes use bugfix path; gaps route; changed implementation hands to code-review | R17 |
| BND-TEMPORAL-001 | temporal-retry | R5, R13, R16, R23 | current, changed, replayed, or identity-mismatched preflight and proof | Mutation preflight and proof identity remain current across the phase transition | Equal identity may continue; changed identity requires new proof or blocks the claim | R13 |
| BND-RECOVERY-001 | failure-recovery | R6, R9, R12, R16, R22, R23 | unavailable command, incomplete proof, interrupted phase, failed check, missing evidence path | Earlier evidence never becomes later authority and partial work never implies completion | Continue diagnosis, route, or block with exact pending work; never overclaim | R16 |
| BND-COMPAT-001 | compatibility-migration | R1, R21, R26 | retained legacy rule, amended rule, removed duplicate, package projection | One current semantic owner remains and shipped projections remain equivalent | Preserved contract ships smaller; lost rule, literal, or parity blocks | R26 |
| BND-ENV-001 | external-environment | R6, R9, R18, R27 | local bounded command, destructive/privileged/network/database effect, external owner | No implicit external or privileged authority and no live acceptance machinery | Safe local evidence may run; unauthorized or unavailable external behavior stops or routes | R6 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R3, R4, R5, R20 | BND-INPUT-001, BND-AUTH-001 | Fix intent or a governed signal is mistaken for broad mutation authority | Resolve exact current authority independently; conflict or invalid signal blocks |
| INT-002 | R10, R11, R12, R16 | BND-STATE-001, BND-RECOVERY-001 | Missing proof blocks the test write needed to create proof, or a broad phase row shadows completion | Permit bounded proof authoring, block production, and select ordered non-overlapping actions |
| INT-003 | R13, R23 | BND-TEMPORAL-001, BND-RECOVERY-001 | A changed proof is presented as the original regression passing | Require identity equality or create a new proof and withhold `fix-applied` |
| INT-004 | R17, R18, R21 | BND-COMPOSE-001, BND-AUTH-001 | Bugfix mutates a contract, design, environment, or external owner surface | Route to the exact owner and preserve read-only boundaries |
| INT-005 | R6, R9, R27 | BND-ENV-001, BND-RECOVERY-001 | Reproduction or acceptance causes unauthorized durable side effects | Require separate authority, skip or stop, and report evidence limits |
| INT-006 | R1, R21, R26 | BND-COMPAT-001, BND-COMPOSE-001 | Compression drops a legacy rule or changes a packaged consumer | Require dispositions, literal inventory, and all package projections to agree |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R3 | BND-INPUT-001 | - | - |
| E2 | illustration | R3 | BND-INPUT-001 | - | - |
| E3 | illustration | R10, R11, R12 | BND-STATE-001 | - | - |
| E4 | illustration | R9, R12 | BND-RECOVERY-001 | - | - |
| E5 | illustration | R17 | BND-COMPOSE-001 | - | - |
| E6 | illustration | R13, R23 | BND-TEMPORAL-001 | - | - |
| E7 | illustration | R14 | BND-INPUT-001 | - | - |
| E8 | illustration | R20, R21 | BND-AUTH-001 | - | - |
| E9 | regression | R16 | BND-STATE-001, BND-RECOVERY-001 | BUGSIM-PR7 | - |
| E10 | illustration | R24 | BND-COMPOSE-001 | - | - |

## Compatibility and migration

The canonical source remains `skills/bugfix/SKILL.md`. No historical bugfix artifact is rewritten. The implementation records a disposition for each behaviorally meaningful legacy rule, preserves consumer-sensitive literals or migrates their consumers atomically, and validates canonical, generated, packed, archived, release-candidate, and installed projections. Rollback reverts the focused contract, skill, fixtures, and directly coupled documentation together.

## Observability

Every result exposes selected operation, authority states, repository and defect scope, current action when stopped or continuing, terminal result on return, commands actually run, proof identity, checks not run, uncertainty, changed surfaces, blockers, and next owner. No hosted or external result is inferred from local evidence.

## Security and privacy

The contract grants no secret, privileged, destructive, network, database, or external-state authority. Sensitive logs and fixtures follow repository policy. Exact path and command scopes prevent an invocation from broadening a concrete defect into unrelated mutation.

## Accessibility and UX

No user interface is introduced. Result labels and closed values remain plain text and machine-readable without relying on color or layout.

## Performance expectations

The implementation adds no runtime. Repository acceptance runs focused deterministic tests before broader package validation. The complete shipped bugfix package must decrease in both normalized word count and UTF-8 bytes.

## Edge cases

EC1. No concrete defect returns `blocked` before command or write authority is inferred.

EC2. Conflicting diagnose and fix wording permits read-only diagnosis but blocks mutation.

EC3. A command advertised as read-only that unexpectedly changes tracked or external state stops and reports the mutation.

EC4. Feasible testing with only an alternative proof selects automated proof authoring, not production correction.

EC5. Infeasible testing with incomplete or subjective alternative evidence blocks.

EC6. A correction whose completed proof later fails selects `stop-blocked`, not a broader correction row.

EC7. A changed fixture between pre-fix and post-fix execution creates a new proof identity.

EC8. A test-defect classification cannot weaken an expectation without settled or restoration evidence.

EC9. Multiple symptoms remain one invocation only when one cause, basis, scope, and proof bundle are established.

EC10. Missing governed evidence placement reports blocked recording without creating lifecycle state.

EC11. A local correction for an external dependency is forbidden unless a settled product resilience contract and exact scope authorize it.

EC12. A successful local fix does not imply review, verification, CI, branch, PR, release, or completion readiness.

## Non-goals

- Creating a diagnosis skill, incident system, issue integration, debugging runtime, test generator, repair engine, or persistent bug transaction.
- Adding packaged references, assets, templates, scripts, or provider-specific procedures.
- Defining project-specific commands, frameworks, or a universal defect taxonomy beyond this control contract.
- Mutating lifecycle state, upstream contracts, review evidence, external systems, or automatically starting downstream gates.
- Executing a live repair task or target-agent runtime as acceptance.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | The package remains one smaller `SKILL.md` with no resource addition. |
| AC2 | Intent, command authority, and write authority classify independently and fail closed. |
| AC3 | Diagnosis-only performs no intentional tracked-file or external-state mutation. |
| AC4 | Every writable fix binds exact repository, defect, authority, command, path, category, contract, and evidence identities. |
| AC5 | Proof-authoring and production-correction gates permit the former without prematurely permitting the latter. |
| AC6 | The proof-action and current-action tables are exhaustive, pairwise non-overlapping, and every action is reachable. |
| AC7 | Post-fix validation uses the unchanged proof identity and failed or mismatched proof prevents `fix-applied`. |
| AC8 | Restoration, contract-gap, test-defect, environment, external-dependency, design, and unknown-cause routing are deterministic. |
| AC9 | Governed signals and evidence placement fail closed without portable fallback or lifecycle creation. |
| AC10 | Exact portable and governed write sets preserve all upstream, lifecycle, review, verification, PR, release, and publication owners. |
| AC11 | Every returning invocation emits one terminal result and changed implementation routes only to `code-review`. |
| AC12 | Rule and literal inventories prove semantic preservation and unknown closed values fail before consistency checks. |
| AC13 | Existing package tooling proves canonical-through-installed parity. |
| AC14 | LF-normalized word and byte measurements both decrease for the root and complete package. |
| AC15 | Acceptance uses deterministic static scenarios and ordinary reviews without live repair, target-agent, or external-system execution. |

## Open questions

None.

## Next artifacts

- Bounded architecture assessment.
- Execution plan and independent plan review.
- Test specification and independent test-spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This specification does not approve itself or authorize implementation.
