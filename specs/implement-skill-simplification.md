# Implement Skill Simplification

## Owning change record

`docs/changes/2026-08-11-implement-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-11-implement-skill-simplification.md`

## Goal and context

This specification defines the behavior-preserving simplification contract for the published `implement` skill package.
It shortens the universal `SKILL.md`, separates planned-milestone and planned-armed automation procedure into two mapped references, and makes one asset the structural owner of implementation results.

The change preserves test-first execution, scope completeness, validation, milestone and correction authority, stop behavior, claim boundaries, and code-review handoff.
It does not certify target-agent behavior, grade model output, or make a numeric size target authoritative over semantic preservation.

This specification specializes `specs/skill-contract.md` for `implement` and operates within the deterministic acceptance boundary established by `specs/published-skill-first-repository-simplification.md`.

## Glossary

- **governing skill package**: canonical `skills/implement/SKILL.md` plus every explicitly mapped reference and structural asset beneath `skills/implement/`, with policy ownership remaining at `implement`.
- **universal contract**: behavior that every valid implementation invocation requires before conditional procedure is loaded.
- **planned milestone context**: a workflow-managed invocation with a valid active plan, one exact current milestone owned by `implement`, and milestone state permitting implementation.
- **armed automation context**: current durable workflow authorization for automated review or correction that matches the same change and planned milestone and is not stale.
- **invocation profile**: one of `IP0-isolated`, `IP1-planned`, or `IP2-planned-armed`.
- **semantic-rule ledger**: change-local accounting for every behaviorally significant current rule or duplicated rule cluster.
- **literal-compatibility inventory**: change-local classification of exact text dependencies and their consumers, separate from semantic preservation.
- **structural result asset**: the mapped copy-and-fill result skeleton that owns labels and layout but no applicability, status, claim, or handoff policy.

## Examples first

### Example E1: isolated implementation loads no conditional procedure

Given a direct or isolated implementation request with clear scope
When neither planned-milestone nor armed-automation evidence exists
Then `SKILL.md` and the core result structure are sufficient and neither conditional procedure reference is loaded.

### Example E2: planned implementation excludes automation procedure

Given valid current planned-milestone evidence and no armed-automation evidence
When implementation begins
Then `planned-milestone-implementation.md` is loaded and `automated-review-correction.md` is not loaded.

### Example E3: planned armed implementation loads both references

Given valid planned-milestone evidence and current matching armed-automation evidence
When automated review or correction procedure is required
Then both conditional references are loaded and remain owned by the `implement` package.

### Example E4: armed but unplanned automation stops

Given armed-automation wording or evidence without a valid current planned milestone
When the invocation is classified
Then implementation stops before conditional procedure is loaded or implementation state is mutated.

### Example E5: result groups follow profile applicability

Given an `IP1-planned` result
When the structural asset is copied and filled
Then the core and planned groups are emitted, the armed group is omitted, and no empty or `not applicable` placeholders remain.

### Example E6: incidental test text does not freeze prose

Given an exact phrase consumed only by a wording-sensitive test and not by a governing contract or parser
When the phrase is simplified
Then the literal inventory classifies it as `test-only-incidental` and the test is updated rather than preserving accidental prose.

### Example E7: runtime execution is rejected as acceptance proof

Given a proposed check would execute Codex, Claude Code, opencode, or another model and grade the response
When acceptance evidence is selected
Then the check is rejected and proof remains deterministic fixtures, repository-owned package checks, and independent semantic review.

## Requirements

R1. The governing published `implement` skill MUST consist of canonical `skills/implement/SKILL.md` plus every explicitly mapped packaged reference and structural asset below the same skill root, while implementation, lifecycle, policy, and readiness ownership remains solely with `implement`.

R2. `SKILL.md` MUST remain sufficient for `IP0-isolated` without loading either conditional implementation reference.

R3. `SKILL.md` MUST keep purpose and trigger, workflow role, authority and prerequisites, test-first behavior, scope-complete first-pass behavior, core validation layering, scope and stop rules, claim boundaries, direct code-review handoff, the compact boundary-first bridge, invocation classification, and every resource load trigger inline.

R4. Invocation classification MUST admit exactly `IP0-isolated`, `IP1-planned`, and `IP2-planned-armed`; armed automation without a planned milestone MUST be invalid.

R5. `planned_milestone_context` MUST require a workflow-managed invocation, a valid active plan, one exact current milestone owned by `implement`, and milestone state permitting implementation; conversational wording alone MUST NOT establish the predicate.

R6. `armed_automation_context` MUST require `planned_milestone_context` plus current durable workflow authorization, the current review or correction mode, matching change and milestone identity, and non-stale authorization evidence.

R7. Missing, stale, mismatched, contradictory, or ambiguous predicate evidence MUST stop before conditional procedure is loaded or implementation state is mutated.

R8. `SKILL.md` MUST map `references/planned-milestone-implementation.md` with the literal verb `READ` and load it exactly for valid `IP1-planned` and `IP2-planned-armed` contexts.

R9. The planned-milestone reference MUST own change-record milestone inspection, baseline change-pack procedure, state synchronization, milestone commit procedure, planned-milestone handoff, and accepted review-fix return to the same milestone; it MUST NOT redefine universal test, validation, stop, claim, or handoff policy.

R10. `SKILL.md` MUST map `references/automated-review-correction.md` with the literal verb `READ` and load it only for valid `IP2-planned-armed` context.

R11. The automation reference MUST own automated review-packet construction, requirement-fidelity routing metadata, forbidden initial context, phase receipts and release conditions, reviewer-declared correction eligibility, bounded correction and rereview, pause or promotion procedure, and final holistic-review prerequisites; it MUST NOT establish planned milestone authority independently.

R12. The two conditional references MAY cite stable concepts or sections in each other but MUST NOT duplicate governing procedure; milestone state and handoff remain planned-reference owned, while automation classification and correction remain automation-reference owned.

R13. `assets/implementation-result-skeleton.md` MUST be the sole copy-and-fill owner of repeated implementation-result labels and layout and MUST NOT own applicability, status meaning, claim authority, correction permission, or handoff policy.

R14. The result asset MUST define: a core group for every valid profile with status, completed scope, changed artifacts, tests, validation and result, blockers, next stage or handoff, and claim limitations; a planned group only for `IP1-planned` and `IP2-planned-armed` with change and milestone identity, plan identity, milestone state, baseline or change-pack status, milestone validation, commit status, and code-review handoff; and an armed group only for `IP2-planned-armed` with automation mode, packet or phase identity, requirement-fidelity routing, correction eligibility and cycle count, rereview requirement, pause or promotion condition, and final holistic-review prerequisite when relevant.

R15. Inapplicable result groups MUST be omitted; unfilled placeholders and meaningless `not applicable` group values MUST be forbidden.

R16. Implementation MUST create `docs/changes/2026-08-11-implement-skill-simplification/implement-rule-disposition.yaml` with stable rule ID, source locations, behavior, governing requirement IDs, applicable profiles, disposition, destination, and preservation proof for every significant rule or duplication cluster.

R17. Semantic-rule disposition MUST use exactly one of `retained-inline`, `retained-planned-reference`, `retained-automation-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; unknown or missing values MUST fail closed before destination consistency checks.

R18. Every significant rule MUST have exactly one disposition; no rule MAY disappear, and obsolete removal MUST cite an approved contract change.

R19. Implementation MUST separately create `docs/changes/2026-08-11-implement-skill-simplification/implement-literal-compatibility.yaml` with literal ID, literal, source location, consumers, classification, required semantics, disposition, and replacement when applicable.

R20. Literal classification MUST use exactly one of `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`; unknown or missing classifications MUST fail closed before treatment consistency checks.

R21. Normative contract literals MUST remain exact unless the governing contract changes; parser or package contracts MUST be preserved or migrated with all consumers atomically; incidental tests MUST be updated instead of owning prose; obsolete literals MUST be removed only with evidence.

R22. Permanent validation MUST enforce only approved contract literals, closed vocabulary, required headings or schema, Resource-map syntax, and package or resource format; the ledgers and size measurements MUST remain change-local evidence and MUST NOT create a new permanent validator family.

R23. Profile measurement MUST use canonical authored files normalized to LF, count each unique loaded resource once, and assemble resources in documented load order.

R24. Change evidence MUST report before-and-after UTF-8 bytes, Unicode whitespace-separated words, and exact resource identities for each profile; it MUST also report `SKILL.md`, each resource, total package, duplicate-cluster, inline-template, and mapped-resource measurements separately.

R25. A token estimate MAY be secondary evidence only when the existing repository tool, version, vocabulary, and normalization are recorded; implementation MUST NOT add a tokenizer dependency for this change.

R26. Acceptance MUST require material reduction for `IP0-isolated` and `IP1-planned`, justified non-regression for `IP2-planned-armed`, complete semantic and literal ledgers, one owner per duplication cluster, honest total-package accounting, and preserved semantic and lifecycle behavior.

R27. The 30–45 percent isolated-profile reduction MUST remain a non-normative planning target; a smaller reduction MUST NOT fail by percentage alone, while no material isolated or planned-profile improvement MUST fail the change objective.

R28. Acceptance proof MUST use deterministic structural proof, fixture-based contract proof, existing package and adapter parity proof, and independent semantic review; fixtures MUST cover the three valid profiles, invalid unplanned automation, stale or mismatched authority, result-group applicability, validation failure, specification gaps, accepted correction return, review handoff, and premature next-milestone transition.

R29. Implementation, verification, release, and repository acceptance MUST NOT execute or grade a target-agent runtime, send prompts, maintain transcript or model-selection evidence, or introduce nondeterministic retry proof.

R30. Existing deterministic owners MUST validate frontmatter, required structure, closed vocabulary, mapped-resource existence and containment, placeholder absence, narrow forbidden claims, generated inventory, canonical-to-generated parity, adapter archive parity, and temporary installed package integrity without a new standalone simplicity validator.

R31. Existing implementation authority, test-first behavior, scope-complete first-pass meaning, validation layering, milestone state, review-fix return, code-review handoff, claim boundaries, and downstream stage ownership MUST remain unchanged except for the explicitly specified resource-loading and result-structure behavior.

R32. The change MUST receive one recorded architecture assessment after approving spec review; `architecture-not-required` is valid only when the existing package model fully covers the new resources and no architecture artifact changes, while ambiguity MUST pause automation.

R33. Rollout MUST update canonical `SKILL.md`, both mapped references, the result asset, ledgers, deterministic fixtures, and package proof atomically; rollback MUST restore the prior complete canonical package and regenerate derived packages without leaving mixed resource ownership.

## Boundary model

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R4, R5, R6, R14, R17, R20, R28 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R5, R6, R7, R9, R11, R31, R32, R33 | BND-STATE-001 | - |
| identity-authority | applicable | R1, R3, R5, R6, R9, R11, R13, R21, R31 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R8, R10, R12, R13, R14, R30 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R6, R7, R9, R11, R28, R31, R33 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R7, R17, R18, R20, R21, R27, R29, R32, R33 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R21, R30, R31, R33 | BND-COMPAT-001 | - |
| external-environment | applicable | R23, R24, R25, R28, R29, R30 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R4, R5, R6, R14, R17, R20, R28 | isolated, planned, planned-armed, invalid unplanned-armed; valid, missing, unknown ledger value | Exactly three profiles are valid; result and ledger values use closed contracts. | Valid profiles load only their resources; invalid profiles stop; unknown values fail closed. | R4 |
| BND-STATE-001 | state-lifecycle | R5, R6, R7, R9, R11, R31, R32, R33 | classify -> load -> implement -> validate -> handoff; correction -> rereview; spec review -> architecture assessment | Conditional procedure never changes workflow or milestone authority, and rollout never mixes package versions. | Valid state advances under existing semantics; stale or invalid state stops; rollback restores one complete package. | R7 |
| BND-AUTH-001 | identity-authority | R1, R3, R5, R6, R9, R11, R13, R21, R31 | `implement`, workflow, plan, milestone, references, asset, validators, tests | Workflow and durable state establish authority; `implement` owns policy; references own procedure; the asset owns structure; tests do not own prose. | Correct owners decide; conversational, stale, mismatched, or incidental authority is rejected. | R1 |
| BND-COMPOSE-001 | composition-path | R1, R2, R8, R10, R12, R13, R14, R30 | `SKILL.md` + boundary reference + planned reference + automation reference + result asset -> generated and packed targets | Universal behavior remains inline; every resource is mapped once; conditional paths do not duplicate policy; package parity holds. | Complete applicable paths pass; missing, duplicated, escaped, stale, or misplaced content fails. | R30 |
| BND-TEMPORAL-001 | temporal-retry | R6, R7, R9, R11, R28, R31, R33 | current authorization, stale authorization, correction cycle, rereview, milestone transition, rollout, rollback | Authority remains bound to the same change and milestone; correction and rereview preserve existing limits. | Current evidence proceeds; stale or premature transitions stop; partial rollout rolls back. | R6 |
| BND-RECOVERY-001 | failure-recovery | R7, R17, R18, R20, R21, R27, R29, R32, R33 | invalid predicate, ledger or literal value, unsafe reduction, runtime-proof request, ambiguous architecture, partial package | Unknown or unsafe conditions fail closed without weakening the last valid contract or package. | Repair routes to the owning spec, ledger, test, package, or architecture surface; runtime proof is rejected. | R7 |
| BND-COMPAT-001 | compatibility-migration | R21, R30, R31, R33 | current prose consumers, parser or package literals, historical evidence, generated targets, rollback package | Contract literals and existing semantics remain valid while incidental wording may change with its tests. | Real contracts migrate atomically; historical evidence remains readable; rollback does not rewrite history. | R31 |
| BND-ENV-001 | external-environment | R23, R24, R25, R28, R29, R30 | canonical filesystem, temporary generated trees, adapters, optional tokenizer, target runtime, network | Acceptance remains repository-owned and deterministic; no new tokenizer or target-runtime dependency is required. | Local proof passes or fails deterministically; unavailable or prohibited runtime proof is omitted or rejected. | R29 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R4, R5, R6, R7 | BND-INPUT-001, BND-AUTH-001, BND-STATE-001 | Armed automation is inferred without the planned milestone it depends on. | The combination is invalid and stops before loading or mutation. |
| INT-002 | R2, R3, R8, R10 | BND-INPUT-001, BND-COMPOSE-001 | Universal implementation policy moves behind a conditional reference. | `IP0-isolated` remains complete from `SKILL.md`; semantic review rejects misplaced policy. |
| INT-003 | R9, R11, R12 | BND-AUTH-001, BND-COMPOSE-001 | Planned and automation references duplicate or exchange authority. | Each reference retains its declared owner boundary and cross-reference duplication is rejected. |
| INT-004 | R13, R14, R15 | BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001 | The result asset emits irrelevant fields or becomes a policy owner. | Only applicable groups appear and all policy remains in the governing instruction resources. |
| INT-005 | R16, R17, R18, R19, R20, R21 | BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001 | An incidental test literal freezes prose or a semantic rule disappears as a wording change. | Separate ledgers preserve semantic policy and migrate only real literal contracts. |
| INT-006 | R23, R24, R25, R26, R27 | BND-ENV-001, BND-RECOVERY-001 | A file-only or unstable token metric hides a planned-profile regression. | Profile words and bytes plus total package metrics expose the delta and semantic acceptance overrides numeric targets. |
| INT-007 | R28, R29, R30 | BND-AUTH-001, BND-ENV-001 | Static contract proof expands into target-runtime execution. | Acceptance stops at deterministic repository proof and independent semantic review. |
| INT-008 | R30, R31, R33 | BND-COMPOSE-001, BND-COMPAT-001, BND-RECOVERY-001 | One generated or installed target receives a stale or partial resource split. | Package validation blocks acceptance and rollback restores one complete prior package. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R4 | BND-INPUT-001 | - | - |
| E2 | illustration | R5 | BND-INPUT-001, BND-STATE-001 | - | - |
| E3 | illustration | R6 | BND-INPUT-001, BND-STATE-001, BND-AUTH-001 | - | - |
| E4 | illustration | R7 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E5 | illustration | R14 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E6 | illustration | R21 | BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001 | - | - |
| E7 | illustration | R29 | BND-RECOVERY-001, BND-ENV-001 | - | - |

## Inputs and outputs

Inputs:

- accepted proposal and approving proposal-review evidence;
- current canonical `implement` package;
- governing skill, workflow, package-integrity, and published-skill-first contracts;
- current plan and workflow state contracts used by planned implementation;
- existing deterministic validators, fixtures, and adapter package targets.

Outputs:

- simplified canonical `SKILL.md`;
- planned-milestone and automated-review/correction references;
- one grouped result asset;
- semantic-rule and literal-compatibility ledgers;
- deterministic profile, result, and package proof;
- before-and-after profile and package measurements;
- independent semantic review evidence.

## State and invariants

- `skills/implement/` remains the only authored package source.
- `implement` remains the only implementation-stage policy owner.
- Exactly three invocation profiles are valid.
- Armed automation always implies the same current planned milestone.
- Universal policy remains inline before conditional loading.
- References own bounded procedure and never independent lifecycle authority.
- The result asset owns structure only and emits only applicable groups.
- Semantic and literal dependencies remain separately accounted.
- Unknown closed values fail before consistency logic.
- Profile reduction never substitutes for semantic preservation.
- Generated, archived, and installed package targets remain derived and equivalent.

## Error and boundary behavior

- Direct wording does not prove planned or armed authority.
- Missing or ambiguous plan or milestone evidence stops before conditional loading.
- Armed automation without the same current planned milestone stops.
- Stale or mismatched automation identity stops.
- A missing, duplicated, escaped, stale, or undeclared mapped resource fails deterministic package proof.
- An unknown or missing ledger disposition or literal classification fails closed.
- A significant rule without one destination blocks semantic preservation.
- A test-only literal is changed with its test rather than promoted to public policy.
- A proposed runtime journey, transcript grade, model selector, or nondeterministic retry is rejected.
- No material isolated or planned-profile improvement fails acceptance even when structure checks pass.
- Architecture ambiguity pauses before planning.
- Partial rollout restores the last complete package.

## Compatibility and migration

Existing implementation status, milestone state, validation, review-fix, handoff, and claim meanings remain valid.
No user data or historical artifact migration is required.

Real parser, package, schema, and normative text dependencies migrate atomically with their consumers.
Incidental wording tests may change with simplified prose.
Historical review records and adapter archives remain historical evidence and are not rewritten.

Rollback restores the prior complete canonical package and regenerates derived targets from that revision.

## Observability

Change-local evidence records:

- invocation-profile resource identities and measurements;
- rule and literal ledger identities, counts, and classifications;
- duplication-cluster owners and result-group applicability;
- deterministic fixture and selected validator outcomes;
- generated, archived, and temporary installed package parity;
- independent semantic review result and residual limitations.

Diagnostics identify the affected artifact, profile or target, violated invariant, and repair surface.
No model identity, prompt, transcript, or runtime retry is recorded as acceptance proof.

## Security and privacy

Acceptance uses repository-local source, fixtures, temporary generated package trees, and review artifacts.
R29 excludes credentials, private prompts, model transcripts, network model access, user data, and machine-local paths from acceptance proof.
R30 requires mapped-resource containment and therefore rejects path traversal outside the skill root.

## Accessibility and UX

No graphical interface is introduced.
The simplified common path, grouped output, and diagnostics use the stable labels, IDs, and actionable stop or repair guidance governed by R3, R13, R14, and R30.

## Performance expectations

R26 requires material loaded-word and UTF-8-byte improvement for `IP0-isolated` and `IP1-planned` and justified non-regression for `IP2-planned-armed`.
The 30–45 percent isolated-profile range remains advisory.
No size metric may override semantic preservation, package parity, or review quality.

## Edge cases

EC1. A rule applies to all profiles: retain it inline even when related planned or automation procedure moves.

EC2. Planned evidence is valid but automation evidence is absent: load only the planned reference and omit the armed result group.

EC3. Automation evidence names another milestone or change: stop as mismatched authority.

EC4. Automation evidence is stale after a correction or state transition: stop and require current workflow authorization.

EC5. A result field carries policy as well as structure: retain policy in the governing instruction and move only its label and layout to the asset.

EC6. A phrase has both parser and test consumers: classify it as `parser-or-package-contract` and migrate all consumers atomically rather than treating it as incidental.

EC7. A rule appears obsolete without an approved contract change: retain it or route the contract change upstream.

EC8. A large `SKILL.md` decrease is achieved by loading more content for `IP1-planned`: fail the change objective.

EC9. The planned and automation references repeat the same milestone transition rule: retain it only in the planned reference and cite it from automation procedure.

EC10. The architecture assessment finds the current package model sufficient but an example is stale: record `architecture-not-required` and update non-architectural documentation only when its owner requires it.

## Non-goals

- Simplifying another skill or changing the standard workflow stage order.
- Changing implementation, milestone, correction, validation, handoff, or downstream authority semantics beyond specified resource loading and result structure.
- Creating a new skill, runtime, service, persistent state, API, or dependency.
- Certifying target-agent interpretation or deterministic model routing.
- Adding prompt journeys, transcript grading, model matrices, runtime-version evidence, or nondeterministic retries.
- Adding permanent simplicity, tokenizer, line-count, word-count, prose-quality, selector, scheduler, cache, or standalone validator machinery.
- Hand-editing generated adapter packages or installed skill copies.
- Rewriting historical review records or adapter archives.

## Acceptance criteria

| ID | Acceptance criterion | Requirement IDs |
| --- | --- | --- |
| AC1 | Exactly three invocation profiles exist; armed automation requires the same valid current planned milestone and identity-bound evidence. | R4-R7 |
| AC2 | Universal authority, test-first, completeness, validation, stop, claim, boundary, trigger, and direct-handoff policy remains inline. | R2, R3 |
| AC3 | The planned reference is loaded only for planned profiles and owns only planned-milestone procedure. | R8, R9 |
| AC4 | The automation reference is loaded only for `IP2-planned-armed` and owns only automation and correction procedure. | R10-R12 |
| AC5 | The result asset is the sole structural owner and emits exactly the applicable core, planned, and armed groups without placeholders or policy. | R13-R15 |
| AC6 | Every significant semantic rule has exactly one valid disposition, destination, profile set, and preservation proof. | R16-R18 |
| AC7 | Every discovered literal dependency has one valid classification and treatment separate from semantic rules. | R19-R22 |
| AC8 | Profile and package measurements use canonical LF-normalized resources, words and bytes, with optional pinned token estimates only. | R23-R25 |
| AC9 | Isolated and planned profiles materially improve, armed context does not grow unjustifiably, and total package changes are reported honestly. | R26, R27 |
| AC10 | Deterministic fixtures prove valid, invalid, stale, mismatched, result-group, failure, correction, and handoff behavior. | R28 |
| AC11 | No acceptance step executes or grades a target-agent runtime or introduces runtime evidence. | R29 |
| AC12 | Existing validators prove skill, resource, generated, archive, and installed-package integrity without a new validator family. | R22, R30 |
| AC13 | Existing implementation, milestone, review, validation, claim, and downstream semantics remain unchanged. | R31 |
| AC14 | A recorded architecture assessment resolves applicability before planning. | R32 |
| AC15 | Rollout and rollback preserve one complete canonical and derived package version. | R30, R33 |

## Open questions

None.

The plan must inventory exact existing validator commands and literal consumers, but those execution details do not alter this contract.

## Next artifacts

- Formal spec review.
- Recorded architecture assessment.
- Architecture and architecture review only when the assessment is `architecture-required`.
- Execution plan and plan review.
- Test specification and test-spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.
Profile authority, resource ownership, output applicability, preservation evidence, deterministic measurement, compatibility, failure behavior, and architecture-assessment obligations are fully specified.
