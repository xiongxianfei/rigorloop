# Explain-Change Skill Simplification

## Owning change record

`docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-18-explain-change-skill-simplification.md`

## Goal and context

Reduce the procedure loaded by portable inline, portable durable, governed inline, and governed durable `explain-change` invocations without weakening actual-diff grounding, evidence truthfulness, lifecycle isolation, final-review binding, refresh safety, or workflow and verification claim boundaries.

The shipped package becomes one compact universal `SKILL.md`, one conditionally read governed-workflow reference, and one copied durable-explanation skeleton. This contract changes package ownership and progressive disclosure; it does not change the standard `explain-change -> verify -> pr` order or grant `explain-change` another stage's authority.

## Glossary

- `governed signal`: an explicit change ID, workflow-managed change identity, structured change-local target, or structured owning-change field that may require governed procedure.
- `reviewed subject`: the exact repository revision and base-to-subject diff covered by final holistic code review.
- `ordered stage-evidence tail`: the two direct-child commits after the reviewed subject that durably record final-review evidence first and the explanation plus workflow handback second.
- `loaded assembly`: the unique set of package resources required by one invocation.
- `Workflow handback`: neutral explain-change-owned state returned to workflow without a readiness conclusion.

## Examples first

Example E1: portable inline explanation
Given no governed signal and no durable-artifact obligation
When the user requests an explanation of an exact local diff
Then `SKILL.md` alone produces an evidence-bounded inline explanation and performs no repository write.

Example E2: governed durable explanation
Given one valid governed candidate, a non-trivial durable obligation, closed review resolution, and a current final holistic review
When `explain-change` runs
Then it loads the governed reference and skeleton, atomically writes the exact explanation artifact, records the reviewed basis, and returns neutral workflow handback.

Example E3: malformed governed signal
Given an owning-change field is present but malformed or conflicts with the workflow identity
When classification occurs
Then the invocation stops before portable output or governed mutation.

Example E4: explicit durable refresh
Given an exact existing portable explanation target and a current explicit user refresh request
When refresh runs
Then the complete artifact is recomposed from the current skeleton and atomically replaces the exact target after identity revalidation.

Example E5: closed ordered stage-evidence tail
Given final code review covers revision `S`, direct-child revision `R` records only final-review-owned evidence and matching workflow transition fields, and direct-child revision `E` records only the governed explanation plus matching workflow handback fields
When verify later checks the handoff
Then the reviewed subject remains `S`, `S -> R -> E` is treated as the closed ordered stage-evidence tail, `E` is the handoff revision, and the final reviewed diff excludes both evidence commits.

Example E6: broader post-review change
Given final code review covers revision `S` and a later commit changes product code, changes a forbidden field, reverses the evidence order, introduces a merge, or adds an unexplained commit
When governed explanation completion or verify evaluates the basis
Then final-review reuse is stale and a fresh final review is required.

Example E7: interrupted ordered evidence recording
Given final-review revision `R` is durably recorded as the direct child of reviewed subject `S` and the explanation revision is not yet present
When the identical governed flow resumes
Then it may create only the exact explanation-and-handback direct child `E`; any changed basis or intervening revision blocks reuse.

## Requirements

R1. The canonical package MUST contain `skills/explain-change/SKILL.md`, `skills/explain-change/references/governed-workflow-explanation.md`, and `skills/explain-change/assets/explain-change-skeleton.md`, and MUST introduce no script, executable generator, tokenizer dependency, or prose-grading runtime.

R2. The universal `SKILL.md` MUST own request routing, project-local evidence and portable defaults, output-action classification, governed-signal classification, actual-diff resolution, evidence-backed traceability, observed/inferred/unknown distinctions, unrelated-change handling, non-goals, risks, validation gaps, sensitive-data exclusions, resource selection, stops, claims, and concise results.

R3. The universal procedure MUST be sufficient to produce a safe portable inline explanation without loading the governed reference or skeleton.

R4. The governed reference MUST own only exact change-root and target validation, non-trivial durable obligations, approved legacy placement, final-review eligibility, review closeout, current workflow-stage interpretation, explanation-basis construction, governed create/refresh procedure, staleness, and workflow handback.

R5. The skeleton MUST own only headings, order, metadata locations, table columns, conditional-group locations, placeholders, and template metadata; it MUST NOT own applicability, authority, evidence sufficiency, staleness, lifecycle policy, or readiness.

R6. Governed-signal classification MUST use exactly `no-governed-signal`, `single-governed-candidate`, and `invalid-or-ambiguous-governed-signal`.

R7. Any present malformed, duplicated, escaped, unsafe, stale, missing-root, mismatched, or conflicting governed signal MUST classify as `invalid-or-ambiguous-governed-signal` and MUST stop without portable fallback.

R8. `single-governed-candidate` MUST load the governed reference before dependent interpretation, but loading MUST NOT grant write, lifecycle, routing, automation, or readiness authority.

R9. Output action MUST use exactly `inline-explanation`, `create-durable-explanation`, and `refresh-durable-explanation` and MUST remain independent from governed-signal classification.

R10. `create-durable-explanation` MUST require one exact absent target; an existing, ambiguous, escaped, conflicting, or unrelated target MUST stop.

R11. `refresh-durable-explanation` MUST require one exact existing target, a known current identity, and either an explicit current user refresh request or a validated governed stale-artifact route.

R12. A missing refresh target MUST route to creation without silently changing the operation, and target existence alone MUST NOT grant refresh authority.

R13. Portable durable authoring MUST require an explicit exact target path or one exact path resolved by project-local contract and MUST NOT create a change root, `change.yaml`, workflow state, review evidence, or governed lifecycle state.

R14. The four loaded assemblies MUST be exactly `EC0-portable-inline` (`SKILL.md`), `EC1-portable-durable` (`SKILL.md` plus skeleton), `EC2-governed-inline` (`SKILL.md` plus governed reference), and `EC3-governed-durable` (`SKILL.md` plus governed reference and skeleton).

R15. Every valid governance/output combination MUST resolve to exactly one assembly, and late discovery MUST load every newly required resource before dependent judgment or mutation.

R16. A missing, unreadable, escaped, mixed-version, or contradictory triggered resource MUST block its dependent assembly; the skill MUST NOT reconstruct missing procedure or structure from memory.

R17. Every durable create and refresh MUST compose the complete artifact from the current skeleton before mutation and MUST NOT perform section-level refresh, mixed-ownership preservation, managed-region editing, or historical-layout parsing.

R18. Historical explanation artifacts MUST remain unchanged unless a genuine create/refresh target-state and authority decision applies; the migration MUST NOT bulk-rewrite history merely to adopt the skeleton.

R19. A durable write MUST resolve the exact action, target, prior identity, reviewed basis, and intended content; validate complete content and identities; re-read every decision-bearing identity; atomically replace the one exact file; and read back the complete result.

R20. When atomic replacement is unavailable, fails, or leaves uncertain bytes, the result MUST be `blocked`; a later invocation MUST classify and resolve current state afresh and MUST NOT adopt unknown, partial, unrelated, ambiguous, or concurrently changed content.

R21. The first version MUST NOT introduce a prepared transaction record, resumable partial-write claim, lifecycle state, or additional persistence owner for the single-file explanation write.

R22. A governed reviewed-change basis MUST identify the change, repository, base revision, reviewed-subject revision, base-to-subject diff identity, final holistic code-review ID and subject identity, applicable proposal/spec/architecture/plan/test-spec identities, review-resolution identity or not-required basis, validation-evidence cutoff, explanation path, and prior target identity.

R23. The final reviewed diff MUST mean the base revision to the reviewed-subject revision and MUST exclude the explanation artifact's recording commit and later verify-owned evidence.

R24. Governed completion MUST represent the reviewed-subject revision, final-review-recording revision, explanation-recording revision, and handoff revision as distinct identities; the explanation artifact MUST record its path, content identity, and reviewed basis without requiring any self-referential commit hash.

R25. Git MUST derive recording and handoff revision identities after their commits exist. Existing workflow or verify evidence MAY consume those derived identities, but `explain-change` MUST write only its exact artifact and MUST NOT acquire authority to mutate review, workflow, or verify evidence.

R26. A workflow-managed governed completion MUST use the exact linear revision sequence `S -> R -> E`: `S` is the reviewed-subject revision, `R` is one direct-child final-review-recording revision, `E` is one direct-child explanation-and-handback revision, and `E` is the handoff revision. Neither `R` nor `E` may be a merge, and no intervening or additional pre-verify revision is permitted.

R27. Revision `R` MUST change only the exact final-review record, review invocation, review log, review-resolution content when required, and the closed workflow-owned transition fields required to record that review. Revision `E` MUST change only the exact explanation artifact and the closed workflow-owned handback fields required to record its path, content identity, evidence pointer, current stage, next stage, blockers, and handoff. Validation MUST enforce both path and field ownership for shared files such as `change.yaml`; path allowlisting alone is insufficient. Neither revision may change product code, tests, specifications, architecture, plans, dependencies, configuration, generated output, unrelated documentation, another artifact's lifecycle state, another stage's evidence, or any unlisted field.

R28. A broader change, forbidden path or field, reversed stage order, merge, non-direct-child relationship, intervening or additional pre-verify commit, changed governing identity, or mismatch between recorded and Git-derived identities MUST stale final-review reuse and require a fresh final holistic review. When only `S -> R` exists and all identities remain current, an identical retry MAY create `E`; it MUST NOT repeat or rewrite `R`.

R29. Later verify-owned evidence after handoff revision `E` MUST NOT stale the explanation when `S -> R -> E`, the governing basis, explanation content, and recorded pre-verify validation cutoff remain unchanged. Verify MUST evaluate the reviewed subject plus the closed ordered tail and MUST NOT include its own later evidence in that pre-verify tail.

R30. A governed durable artifact MUST record `Stage: explain-change`, `Status: current`, the final reviewed diff identity, final review identity, and every other decision-bearing identity required for staleness checks.

R31. Material review findings MUST be summarized by final disposition and linked to exact review resolution; open findings, `Closeout status: open`, or `needs-decision` MUST block governed explanation completion.

R32. The conditional durable group MUST be named `Workflow handback`, and its closed fields MUST report explanation status (`current` or `blocked`), explanation basis, validation-evidence cutoff, open explain-change blockers, whether control returned to workflow, and `workflow` as next-stage decision owner.

R33. Portable inline output MUST omit `Workflow handback`; portable durable output MUST omit it unless project contract requires neutral metadata; governed inline output MUST report the facts in its result; governed durable output MUST include it for complete or blocked outcomes.

R34. `Workflow handback` and all explain-change results MUST NOT claim or imply verify readiness or passage, branch readiness, PR-body or PR-open readiness, hosted CI completion, release readiness, deployment readiness, or lifecycle completion.

R35. Only workflow MAY decide whether verify is next, and direct or isolated `explain-change` MUST stop after its own result without workflow-continuation claims.

R36. The migration MUST maintain separate semantic-rule and literal-consumer ledgers and MUST give every current rule, heading, metadata label, path, result value, readiness phrase, and parser-sensitive literal one disposition and owner.

R37. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST include an unknown-value regression test.

R38. Measurement MUST use LF-normalized canonical authored files, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded or copied file exactly once per assembly.

R39. Measurement MUST report `EC0`, `EC1`, `EC2`, `EC3`, `SKILL.md`, the governed reference, the skeleton, and total package size separately.

R40. Each of `EC0`, `EC1`, `EC2`, and `EC3` MUST strictly decrease in both words and UTF-8 bytes from the frozen 1,175-word and 8,224-byte flat baseline; estimated tokens MAY supplement but MUST NOT replace exact gates.

R41. Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode package resources MUST preserve required inventory and raw-byte parity through existing repository tooling.

R42. Published skill text MUST remain project-portable and MUST keep repository-maintainer source paths, generated mirrors, adapter mechanics, selector constraints, drift checks, and release procedure in contributor or governing surfaces rather than shipped procedure.

R43. Acceptance MUST use deterministic contract, fixture, validator, lifecycle, package, parity, and measurement proof and MUST NOT execute a target-agent runtime or add a separate manual semantic-review or prose-grading gate.

R44. The bounded architecture assessment MUST return `architecture-required` if safe implementation needs a new persistent reviewed-subject/evidence-tail identity model, transaction record, machine-readable schema owner, lifecycle state, routing owner, cross-stage write authority, or executable generator.

## Inputs and outputs

Inputs are the approved portable proposal and review evidence, current `explain-change` skill, workflow and skill-package contracts, final-review and explanation consumers, validators, fixtures, generated-package metadata, and project-local routing evidence.

Outputs are the simplified canonical package, focused contract and proof-map updates, semantic and literal ledgers, deterministic scenarios, assembly measurements, package parity evidence, and stage-owned lifecycle evidence.

## State and invariants

- `skills/` remains the only authored skill source.
- Governance and durability remain independent axes.
- The reviewed subject does not change when final-review evidence, the explanation, or workflow handback is recorded.
- `explain-change` writes only its exact explanation artifact.
- Final code review, workflow routing, verify, and PR retain their current authority.
- Historical artifacts remain historical unless explicitly refreshed.
- Every real assembly improves; root-only reduction is insufficient.

## Error and boundary behavior

Unknown vocabulary, invalid governed signals, ambiguous output action, unsafe or missing paths, stale final review, open review resolution, changed governing identities, absent refresh authority, missing triggered resources, non-atomic or uncertain replacement, broader evidence tails, parser drift, package drift, and forbidden readiness claims fail closed with an exact blocker and owner.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R6, R7, R9, R10, R11, R12, R13, R32, R37 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R10, R11, R12, R18, R20, R22, R23, R24, R26, R27, R28, R29, R30, R31 | BND-STATE-001 | - |
| identity-authority | applicable | R7, R8, R10, R11, R13, R22, R25, R26, R27, R28, R31, R35 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R14, R15, R16, R17, R32, R33, R41, R42 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R11, R15, R19, R20, R23, R24, R26, R27, R28, R29 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R16, R19, R20, R21, R28, R31, R44 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R17, R18, R32, R34, R36, R37, R38, R39, R40, R41, R42 | BND-COMPAT-001 | - |
| external-environment | applicable | R13, R16, R19, R20, R25, R26, R27, R41, R43 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R6, R7, R9, R10, R11, R12, R13, R32, R37 | three signal classes, three output actions, target absent/existing/ambiguous, refresh authority present/absent, handback values, and unknown values | exactly one closed value applies and unknowns fail before consistency checks | one valid operation proceeds or classification stops | R6 |
| BND-STATE-001 | state-lifecycle | R10, R11, R12, R18, R20, R22, R23, R24, R26, R27, R28, R29, R30, R31 | target absent/existing, reviewed subject current/stale, no tail/review-only partial tail/complete ordered tail/broader tail, review resolution closed/open, and artifact current/blocked | later stage evidence never redefines the reviewed subject or settles another stage | current output, identical completion of `S -> R -> E`, or exact stale/blocked result | R23 |
| BND-AUTH-001 | identity-authority | R7, R8, R10, R11, R13, R22, R25, R26, R27, R28, R31, R35 | portable request, governed candidate, user refresh, stale-artifact route, final review recording, explanation write, workflow handback, verify evidence, and forbidden cross-stage writes | loading, commit composition, target existence, and handback never broaden any stage's write authority | each owner contributes only its closed paths and fields or the operation stops | R11 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R14, R15, R16, R17, R32, R33, R41, R42 | four assemblies, universal root, conditional reference, copied skeleton, inline result, durable artifact, and packaged copies | each rule and structure has one owner and required resources are exact | correct assembly loads or dependent work blocks | R14 |
| BND-TEMPORAL-001 | temporal-retry | R11, R15, R19, R20, R23, R24, R26, R27, R28, R29 | initial write, exact refresh, concurrent change, atomic failure, fresh retry, `S -> R -> E`, review-only interruption, and later verify evidence | current identities and strict ancestry are reread and no uncertain or reordered output is adopted | atomic file completion, exact stage-tail continuation, fresh retry, or stale/blocked result | R19 |
| BND-RECOVERY-001 | failure-recovery | R16, R19, R20, R21, R28, R31, R44 | missing resource, pre-write failure, uncertain replacement, unrelated partial bytes, open review, and new persistence need | recovery reconstructs neither missing procedure nor unknown content | unchanged stop, fresh operation, or architecture escalation | R20 |
| BND-COMPAT-001 | compatibility-migration | R17, R18, R32, R34, R36, R37, R38, R39, R40, R41, R42 | flat package, split package, historical artifact, refreshed artifact, old readiness label, new handback label, semantic rule, consumed literal, and package forms | history is not bulk rewritten and semantic/literal ownership and parity remain explicit | prospective migration passes atomically or blocks | R36 |
| BND-ENV-001 | external-environment | R13, R16, R19, R20, R25, R26, R27, R41, R43 | portable project, governed repository, filesystem atomic capability, Git revision graph, path-and-field diff inspection, generated adapters, clean install, and unavailable environment | claims match inspected local evidence and no external system is mutated | local deterministic proof succeeds or dependent action blocks | R43 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R6, R7, R8, R13, R14, R15 | BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001 | malformed governed evidence falls through to portable output or late discovery uses an underloaded assembly | invalid signals stop; valid late signals load the governed procedure before interpretation |
| INT-002 | R10, R11, R12, R17, R19, R20 | BND-INPUT-001, BND-TEMPORAL-001, BND-RECOVERY-001 | create replaces an existing artifact or refresh overwrites concurrent or uncertain content | exact authority and identities precede one current-skeleton atomic replacement; uncertainty blocks |
| INT-003 | R22, R23, R24, R25, R26, R27, R28, R29 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | durable final-review recording and later explanation recording become circular, self-stale, reordered, or broad enough to conceal implementation drift | the reviewed subject remains fixed; only exact linear `S -> R -> E` with closed path-and-field ownership is reusable |
| INT-004 | R30, R32, R33, R34, R35 | BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001 | a structural handback field claims routing or readiness | handback exposes only explanation-owned facts and names workflow as decision owner |
| INT-005 | R2, R4, R5, R14, R16, R36, R38, R39, R40, R41 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | relocation hides semantic loss, grows a real assembly, or ships drifted resources | ledgers, every-assembly gates, and package parity all pass |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R3, R14 | BND-COMPOSE-001 | - | - |
| E2 | illustration | R14, R32 | BND-COMPOSE-001 | - | - |
| E3 | regression | R7 | BND-INPUT-001, BND-AUTH-001 | EXCSIM-PR1 | - |
| E4 | regression | R11 | BND-INPUT-001, BND-TEMPORAL-001 | EXCSIM-PR4 | - |
| E5 | regression | R26, R27 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | EXCSIM-CR2 | - |
| E6 | regression | R28 | BND-AUTH-001, BND-TEMPORAL-001 | EXCSIM-PR5 | - |
| E7 | regression | R26, R28 | BND-STATE-001, BND-TEMPORAL-001 | EXCSIM-CR2 | - |

## Compatibility and migration

The split is prospective. Existing explanation artifacts remain readable and unchanged until explicitly refreshed. A genuine refresh replaces the complete artifact using the current skeleton; no section parser or managed-region compatibility layer is introduced. The canonical skill, new reference and asset, focused contract, consumers, validators, fixtures, mappings, and generated package inventories migrate atomically. Rollback restores the prior flat skill and coupled expectations and removes the two mapped resources without rewriting existing explanations.

The parser-sensitive `Final diff identity` and `Final review identity` remain supported while the focused contract clarifies that final diff means base-to-reviewed-subject. Any existing `Verify readiness` consumer must migrate atomically to `Workflow handback`; no misleading readiness alias remains in newly authored explanations.

## Observability

The change is observable through classified signals, selected action and assembly, exact target and identities, blockers, explanation-basis metadata, workflow-handback fields, semantic and literal ledgers, assembly measurements, deterministic scenarios, lifecycle validation, and canonical-through-installed parity. Configured commands remain distinct from executed evidence.

## Security and privacy

Universal procedure must exclude secrets, credentials, private keys, unnecessary personal data, machine-local paths, inaccessible evidence, and unsafe transcript excerpts. Governed paths must remain within the validated change root and portable paths within the exact authorized project target. No external system mutation is introduced.

## Accessibility and UX

No end-user UI is added. Published Markdown must remain readable, use complete sentences, stable labels, and accessible tables, and emit no placeholders or ambiguous readiness language.

## Performance expectations

All four assemblies must use fewer words and bytes than the current flat baseline. No runtime latency, network, service-level, or target-agent performance contract is introduced.

## Edge cases

EC1. The user requests durable output without an exact portable path: durable output blocks and no governed root is created.

EC2. The target appears between classification and create: identity re-read blocks replacement.

EC3. A refresh is requested for a missing target: the result routes to creation without mutating.

EC4. A governed signal appears only after initial portable classification: the governed reference loads before any dependent output.

EC5. The skeleton is missing for a durable action: the operation blocks even when the governed reference is present.

EC6. Atomic replacement succeeds but read-back differs: completion is not claimed and current bytes are treated as uncertain.

EC7. The reviewed subject is unchanged but verify later records evidence: the explanation remains current for its pre-verify cutoff.

EC8. Revision `E` changes the explanation and an authorized workflow-handback field in `change.yaml`: field-scoped validation permits those exact changes, while any unlisted `change.yaml` field blocks final-review reuse.

EC9. A historical explanation uses a different heading order: it remains unchanged until an authorized refresh, which then uses the current skeleton.

EC10. `EC0` shrinks but `EC3` grows beyond baseline: acceptance fails.

## Non-goals

- Changing lifecycle order, final-review authority, review-resolution semantics, verification ownership, PR ownership, or trivial/non-trivial classification.
- Adding section-level refresh, managed Markdown ownership, historical-layout parsing, or bulk historical migration.
- Adding executable generation, semantic grading, target-agent benchmarking, a tokenizer dependency, or a new transaction/evidence service.
- Creating a new lifecycle state, routing owner, cross-stage write authority, or persistence schema; the ordered tail composes existing owners without transferring their authority.
- Optimizing another skill except directly coupled contracts, validators, fixtures, package mappings, and generated outputs.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every R-clause maps to direct deterministic proof in the test specification. |
| AC2 | The package has one universal skill, one governed reference, one skeleton, and no script. |
| AC3 | Every governance/output combination selects exactly one of four assemblies and invalid signals never fall through. |
| AC4 | Create and refresh use exact target-state and authority rules and every durable action uses current-skeleton whole-file composition. |
| AC5 | Atomic replacement, concurrency, uncertain output, and fresh retry have fail-closed deterministic outcomes. |
| AC6 | The reviewed subject, final-review recording, explanation recording, handoff revision, and ordered stage-evidence tail remain distinct and traceable without self-reference. |
| AC7 | Only exact linear `S -> R -> E` with closed path-and-field ownership preserves final-review reuse; every broader, reordered, merged, intervening, or unknown tail stales it. |
| AC8 | `Workflow handback` reports only explanation-owned facts and no readiness claim. |
| AC9 | Historical explanations are not bulk migrated, while genuine refreshes adopt the current skeleton. |
| AC10 | Semantic and literal ledgers cover every current rule and consumed literal. |
| AC11 | All four assemblies decrease in words and bytes and total package size remains visible. |
| AC12 | Canonical-through-installed inventories and raw bytes match across supported adapters. |
| AC13 | Unknown closed-vocabulary values fail before consistency checks and receive regression coverage. |
| AC14 | Acceptance executes no target-agent runtime and adds no manual semantic-review or prose-grading gate. |
| AC15 | Architecture becomes required if the implementation needs a new identity, transaction, schema, lifecycle, routing, or cross-stage authority owner. |

## Open questions

None. Exact metadata field serialization and fixture names may be settled in planning and the test specification while preserving R22 through R30.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Execution plan and test specification after review settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This artifact does not claim review approval, architecture settlement, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
