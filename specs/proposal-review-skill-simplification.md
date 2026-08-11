# Proposal-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-11-proposal-review-skill-simplification.md`

## Goal and context

Simplify the published `proposal-review` skill so ordinary advisory review loads a compact universal judgment contract while durable recording, formal settlement, automation, and specialized proposal gates load only when current evidence requires them.

The change preserves proposal judgment, formal-review recording, lifecycle ownership, isolation, material-finding rigor, status and claim semantics, installed-skill artifact placement, and package integrity.
It changes instruction composition and structural ownership, not review outcomes, workflow stage order, change metadata, or downstream authority.

## Glossary

- `recording mode`: exactly `none`, `advisory-durable`, or `formal-lifecycle`; it controls durable write and settlement permissions.
- `automation mode`: exactly `manual` or `workflow-managed-automated`; it controls automation-only review procedure independently of recording mode.
- `durable_recording_context`: a closed predicate true for formal lifecycle review, explicit durable-record request, any material finding, or an outcome of `changes-requested`, `blocked`, or `inconclusive`.
- `specialized-gate context`: one or more of `vision_exception_context`, `standing_artifact_context`, and `scope_budget_context` established from current review evidence.
- `recording-only root`: the minimal change-local root created under the formal-review-recording contract to preserve review evidence; it grants neither artifact settlement nor workflow continuation authority.
- `resource assembly`: exactly one of `PRR0-core`, `PRR0G-context-gated`, `PRR1-recorded`, and `PRR1G-recorded-context-gated`.
- `result group`: one universal core group or one of four conditional groups in the result asset.

## Examples first

### Example E1: clean advisory review stays on the common path

Given a direct advisory review has no durable request, material finding, non-approval outcome, or specialized-gate evidence
When proposal judgment completes
Then the invocation uses `PRR0-core`, records no durable artifact, reports the advisory result, and stops without workflow continuation.

### Example E2: material evidence activates recording late

Given a review begins in `recording_mode: none`
When judgment establishes a material finding
Then the skill reclassifies to `advisory-durable`, loads the recording reference before any required write or recording claim, and preserves isolation from settlement and continuation.

### Example E3: material advisory review can create a recording-only root

Given a material advisory review has no existing owning change root or explicit change ID
When the formal-review-recording selection order yields an unambiguous generated fallback
Then the skill creates the required minimal recording-only root and does not settle the reviewed proposal, activate workflow, or authorize downstream continuation.

### Example E4: formal lifecycle review has bounded settlement authority

Given current governed evidence identifies this exact proposal review for the same change
When formal review recording succeeds
Then the skill records formal evidence and settles only the proposal review entry, while workflow retains continuation authority.

### Example E5: automated review requires formal authority

Given automation is requested without current formal governed authority for the same proposal and change
When the invocation is classified
Then the combination is invalid and stops before an automation packet, receipt, correction, or settlement write.

### Example E6: specialized predicates compose

Given both vision-exception and scope-budget evidence are current
When specialized review begins
Then the conditional-gates reference loads once and applies both gates without changing recording or automation authority.

### Example E7: result groups follow classified context

Given a formal automated review also triggers a specialized gate
When the result is rendered
Then the asset includes core, specialized-gate, durable-recording, formal-settlement, and automated-review groups, with no unfilled placeholders or policy in the asset.

### Example E8: a required resource failure stops safely

Given late material evidence requires the recording reference
When that mapped reference is missing or unreadable
Then the skill stops before the dependent write or recording claim and does not reconstruct procedure from memory.

## Requirements

R1. The published package MUST remain owned by `skills/proposal-review/` and MUST contain canonical `SKILL.md`, `references/proposal-review-recording-and-settlement.md`, `references/conditional-proposal-gates.md`, `assets/review-result-skeleton.md`, and `assets/material-finding.md` as its complete authored package.

R2. `SKILL.md` MUST be self-sufficient for valid core advisory review, including target and authority resolution, evidence reading, core proposal judgment, materiality, severity, status, readiness, isolation, stops, claims, resource selection, and handoff limits.

R3. Universal proposal judgment MUST continue to cover problem clarity, user value, option diversity, rationale, vision fit, scope and initial-intent preservation, risk, rollout, testability, architecture awareness, and readiness for specification.

R4. `SKILL.md` MUST retain the default formal record path `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` and MUST retain the shared governed `## Isolation and Recording` contract required by the formal-review-recording specification.

R5. Recording mode MUST be exactly `none`, `advisory-durable`, or `formal-lifecycle`, and automation mode MUST be exactly `manual` or `workflow-managed-automated`; unknown, missing, contradictory, or unsupported values MUST fail closed before side effects.

R6. The only valid mode combinations MUST be `none/manual`, `advisory-durable/manual`, `formal-lifecycle/manual`, and `formal-lifecycle/workflow-managed-automated`; the two other automated combinations MUST stop.

R7. `durable_recording_context` MUST be true for formal lifecycle review, an explicit durable-record request, at least one material finding, or status `changes-requested`, `blocked`, or `inconclusive`, and false only when none applies.

R8. A review that begins without durable context MUST reclassify and load the recording reference before a late finding, outcome, or explicit request causes a required durable write or recording claim.

R9. The recording-and-settlement reference MUST own detailed change-root lookup, clean receipt versus detailed record selection, material record and log synchronization, resolution requirements, formal proposal settlement, bounded retry handling, automation packets and receipts, correction boundaries, and workflow-managed handoff mechanics.

R10. Loading the recording reference MUST NOT grant formal settlement, automation, correction, or continuation authority; those permissions MUST derive from the independently classified modes and current same-change evidence.

R11. `advisory-durable/manual` MAY write authorized review evidence but MUST NOT settle proposal lifecycle state, report formal next-stage eligibility, advance workflow, or write automation evidence.

R12. `formal-lifecycle/manual` and `formal-lifecycle/workflow-managed-automated` MUST write required formal review evidence and MAY settle only the exact proposal review entry when current authority identifies the same proposal and change; neither mode MAY advance workflow.

R13. Only `formal-lifecycle/workflow-managed-automated` MAY use neutral review packets, phase receipts, independence checks, automation correction procedure, or automation-specific pause and handoff evidence, and correction still requires separately valid correction authority.

R14. Clean non-formal advisory recording requested explicitly MAY use a valid user path or project-local advisory location without creating formal log, resolution, settlement, or workflow state.

R15. Material, non-approval, blocked, inconclusive, and formal recording MUST use the change-ID selection order governed by `specs/formal-review-recording.md`: existing active root, reviewed-artifact metadata, explicit user ID, then generated `YYYY-MM-DD-<subject>-review-recording` fallback.

R16. A safe generated fallback MUST create only the minimal artifacts required by the formal-review-recording contract and MUST remain a recording-only root unless separate exact governed authority permits proposal settlement.

R17. Ambiguous identity, unrelated-root collision, unsafe path, or failed write MUST produce blocked recording, preserve complete findings in the invocation output, and claim neither durable recording nor formal completion.

R18. The conditional-gates reference MUST own detailed vision-exception, standing-artifact or bootstrap, and broad scope-budget procedure only; ordinary vision, intent, and scope judgment MUST remain inline.

R19. Specialized predicates MUST use exactly `vision_exception_context`, `standing_artifact_context`, and `scope_budget_context`, MUST be classified by proposal-review judgment from bounded evidence, and MUST NOT be semantically inferred by deterministic validators.

R20. Every true specialized predicate MUST be applied, the gates reference MUST load once for any non-empty predicate set, late predicate discovery MUST complete before final status, and unresolved predicate ambiguity MUST block approval.

R21. Resource assembly MUST use exactly `PRR0-core`, `PRR0G-context-gated`, `PRR1-recorded`, and `PRR1G-recorded-context-gated`, with durable and specialized predicates independently additive.

R22. A conditional reference MAY specialize its owned procedure but MUST NOT override an inline universal rule or another reference's owned contract; any contradiction MUST stop dependent work as a package defect.

R23. A missing or unreadable triggered reference or asset MUST stop before dependent judgment, writing, settlement, rendering, or handoff; an untriggered reference MUST not load or block an otherwise valid review; memory-based reconstruction MUST be forbidden.

R24. `review-result-skeleton.md` MUST be the sole overall result structure and MUST contain one core group plus specialized-gate, durable-recording, formal-settlement, and automated-review conditional groups.

R25. The core result group MUST apply to every review; the specialized group MUST apply exactly when a specialized predicate is true; the durable group MUST apply exactly when recording mode is not `none`; the formal group MUST apply exactly in `formal-lifecycle`; and the automated group MUST apply exactly in `workflow-managed-automated`.

R26. Inapplicable result groups MUST be omitted; applicable groups with unavailable required data MUST report explicit `blocked` or `unknown` state and blocker; unfilled placeholders MUST be forbidden.

R27. The result asset and material-finding asset MUST own labels, order, and repeated structure only; `SKILL.md` and references MUST retain applicability, meaning, status, severity, recording, settlement, correction, claim, and handoff policy.

R28. Existing material-finding required fields, severity vocabulary, review-status vocabulary, proposal-readiness meaning, recording status, formal settlement, and handoff semantics MUST remain unchanged.

R29. A change-local semantic rule-disposition ledger MUST give every behaviorally significant current rule a stable ID, sources, behavior, governing requirements, applicable assemblies, one closed disposition, destination, and preservation proof.

R30. Semantic dispositions MUST be exactly `retained-inline`, `retained-recording-reference`, `retained-conditional-gates-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; unknown or missing values MUST fail closed before consistency checks.

R31. A separate literal-compatibility inventory MUST classify every exact dependency as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`, record consumers and replacement, preserve contract literals, migrate parser consumers atomically, and avoid promoting incidental tests to policy.

R32. Measurement MUST normalize canonical resources to LF, count each unique loaded resource once in documented order, and report UTF-8 bytes and Unicode whitespace-separated words for `SKILL.md`, every resource, every valid assembly, and the total package.

R33. The 30-45 percent common-path reduction MUST remain advisory; acceptance MUST require material common-path reduction, complete disposition, one owner per duplication cluster, separate total-package accounting, and semantic preservation.

R34. Acceptance MUST use deterministic structural checks, static contract scenarios, existing package-chain proof, and independent semantic review; it MUST NOT execute a target-agent runtime or add prompt journeys, transcript grading, runtime certification, a permanent simplicity validator, or a new tokenizer dependency.

R35. Existing validation owners MUST prove normalized structure, closed vocabularies, resource-map syntax, resource containment, placeholder absence, canonical/generated/packed/installed inventory, and required raw-byte resource parity.

R36. A recorded architecture assessment MUST precede planning and MUST select `architecture-not-required` when the existing package model remains accurate; if implementation requires an architecture change, this change MUST own and review the architecture artifact.

R37. Rollout and rollback MUST operate on one complete canonical package revision plus directly coupled contract and literal consumers; mixed or partial resource versions MUST fail package validation and dependent runtime procedure.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R5, R6, R7, R14, R15, R19, R20 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R7, R8, R10, R11, R12, R13, R16, R17, R36, R37 | BND-STATE-001 | - |
| identity-authority | applicable | R10, R11, R12, R13, R14, R15, R16, R17 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R9, R18, R21, R22, R23, R24, R25, R26, R27, R35 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R8, R9, R12, R13, R17, R20, R37 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R5, R6, R17, R20, R22, R23, R26, R30, R31, R36, R37 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R4, R28, R29, R30, R31, R35, R36, R37 | BND-COMPAT-001 | - |
| external-environment | applicable | R14, R15, R16, R17, R23, R32, R34, R35, R37 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R5, R6, R7, R14, R15, R19, R20 | valid and invalid mode pairs; durable true or false; three specialized predicates; existing, metadata, explicit, generated, ambiguous identity | one closed classification governs each decision; ambiguity never becomes false | valid assembly and mode, or fail-closed stop | R5 |
| BND-STATE-001 | state-lifecycle | R7, R8, R10, R11, R12, R13, R16, R17, R36, R37 | none to durable reclassification; advisory versus formal settlement; manual versus automated; complete versus partial rollout | loading never grants authority; only owners write their state | authorized evidence and settlement, or explicit blocker | R10 |
| BND-AUTH-001 | identity-authority | R10, R11, R12, R13, R14, R15, R16, R17 | direct user, formal workflow, proposal-review, workflow, and recording-root authority; same or mismatched identity | recording does not imply settlement; settlement does not imply continuation | bounded write, formal eligibility report, or authority stop | R12 |
| BND-COMPOSE-001 | composition-path | R1, R2, R9, R18, R21, R22, R23, R24, R25, R26, R27, R35 | four assemblies; two references; two assets; five result groups; canonical through installed resources | each rule and structure has one owner; triggered resources are complete | exact assembly and structurally valid result | R21 |
| BND-TEMPORAL-001 | temporal-retry | R8, R9, R12, R13, R17, R20, R37 | early or late trigger; current or stale authority; retry after blocked write; before or after atomic package revision | final classification uses current evidence and precedes dependent effects | reclassified completion, safe retry, or stop | R8 |
| BND-RECOVERY-001 | failure-recovery | R5, R6, R17, R20, R22, R23, R26, R30, R31, R36, R37 | unknown vocabulary; ambiguity; missing resource; blocked group; package conflict; partial migration | failure remains visible and never invents policy or authority | explicit blocker, owner correction, or atomic rollback | R23 |
| BND-COMPAT-001 | compatibility-migration | R4, R28, R29, R30, R31, R35, R36, R37 | semantic and literal dispositions; prior and current packages; rollout and rollback | significant rules never disappear and consumers migrate together | compatible current package or complete prior revision | R31 |
| BND-ENV-001 | external-environment | R14, R15, R16, R17, R23, R32, R34, R35, R37 | writable or unwritable roots; canonical, generated, packed, installed filesystems; target runtime present or absent | acceptance is deterministic and package based; paths remain contained | recorded proof, package blocker, or safe omission of runtime proof | R34 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R7, R8, R9, R17, R21 | BND-INPUT-001, BND-TEMPORAL-001, BND-COMPOSE-001 | a late finding could be emitted before required recording procedure loads | reclassify, load the reference, record or report blocked, then emit the result |
| INT-002 | R10, R11, R12, R15, R16 | BND-AUTH-001, BND-STATE-001 | a generated recording root could be mistaken for settlement authority | create required evidence while withholding settlement and continuation |
| INT-003 | R18, R19, R20, R21 | BND-INPUT-001, BND-COMPOSE-001 | combined or late predicates could omit a specialized gate | load once, apply every current predicate, and block unresolved ambiguity |
| INT-004 | R23, R25, R26 | BND-COMPOSE-001, BND-RECOVERY-001 | a required resource may disappear after classification | stop the dependent action and render no invented or partial structure |
| INT-005 | R29, R30, R31, R32, R33 | BND-RECOVERY-001, BND-COMPAT-001 | size pressure or incidental tests could remove semantics | closed ledgers and semantic review govern; size remains advisory |
| INT-006 | R34, R35, R37 | BND-COMPOSE-001, BND-ENV-001 | one package target could omit or transform a mapped resource | existing package-chain checks prove complete raw-byte-consistent resources |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R7 | BND-INPUT-001 | - | - |
| E2 | illustration | R8 | BND-TEMPORAL-001 | - | - |
| E3 | illustration | R15, R16 | BND-AUTH-001, BND-ENV-001 | - | - |
| E4 | illustration | R10, R12 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | illustration | R6 | BND-INPUT-001, BND-RECOVERY-001 | - | - |
| E6 | illustration | R19, R20 | BND-INPUT-001 | - | - |
| E7 | illustration | R24, R25, R26 | BND-COMPOSE-001 | - | - |
| E8 | illustration | R23 | BND-RECOVERY-001, BND-ENV-001 | - | - |

## Inputs and outputs

Inputs are the reviewed proposal and identity, invocation authority, current change-local metadata, applicable standing artifacts, initial user intent, bounded repository evidence, review findings, recording request, and current packaged resources.

Every result records review target, recording mode, automation mode, review status, material finding IDs or none, blockers, proposal readiness, immediate next stage, automatic handoff, and claim limitations.
Conditional result groups record specialized gates, durable evidence, formal settlement, and automation evidence only when applicable.

## State and invariants

- Resource loading, recording mode, automation mode, settlement authority, and continuation authority are separate decisions.
- Formal review recording follows `specs/formal-review-recording.md`; this specification does not redefine its artifact schemas or change-ID rules.
- A recording-only root never grants settlement or workflow authority.
- Specialized predicates change review procedure, not recording or automation authority.
- Assets own structure only, and references remain procedure owned by the `proposal-review` package.
- Rule and literal inventories are change-local proof rather than recurring product state.

## Error and boundary behavior

- Unknown closed vocabulary fails before consistency checks.
- Ambiguous recording identity produces blocked recording with complete findings preserved.
- Missing triggered resources stop before dependent action and are not reconstructed.
- Applicable unavailable result data is explicit rather than an empty placeholder.
- Formal completion without required evidence or exact settlement identity is forbidden.
- Isolated recording never advances workflow.

## Compatibility and migration

Existing review statuses, severity, finding shape, review recording, artifact settlement, lifecycle ownership, output meaning, and handoff behavior remain compatible.
The migration relocates conditional procedure and structural duplication but does not migrate project data or change the `change.yaml` schema.

Canonical skills, references, assets, directly coupled literal consumers, generated packages, archives, and installed-package proof roll out atomically.
Rollback restores the complete prior canonical package and consumer set, then regenerates and revalidates derived packages.

## Observability

Change evidence records the semantic rule ledger, literal inventory, static scenarios, before and after measurements, per-assembly resources, duplicate-cluster disposition, package-chain proof, and independent semantic review.
Every validation record names the exact command, result, owner, and evidence location.
Target-runtime transcripts and model identities are not acceptance evidence.

## Security and privacy

The change introduces no network, credential, secret, user-data, publication, or external-action requirement.
Path containment, safe identity selection, and collision checks prevent writes to unrelated change roots.
Static fixtures and package proof remain repository-local.

## Accessibility and UX

No graphical interface changes.
The shorter common path, closed modes, concise result groups, and explicit diagnostics improve scanability without reducing review detail.

## Performance expectations

`PRR0-core` loaded words and bytes MUST be materially lower than the baseline without semantic loss.
The 30-45 percent reduction is advisory and total package size is reported separately.
No runtime latency, model-token, or review-quality percentage guarantee is introduced.

## Edge cases

EC1. A clean advisory review becomes `changes-requested` without a material finding; durable recording still activates.

EC2. A generated fallback collides with an unrelated root; recording is blocked and the finding remains in output.

EC3. A clean explicit advisory record uses a standalone allowed path; no formal log or settlement is created.

EC4. A formal review can record into a fallback root but lacks exact reviewed-proposal identity; recording succeeds while settlement remains blocked.

EC5. Two specialized predicates activate after core judgment begins; both gates run once before status selection.

EC6. An installed adapter contains `SKILL.md` but omits one triggered reference; dependent review fails safely and package validation fails.

EC7. A conditional group is applicable but its receipt path is unavailable; the group reports `blocked` with the blocker.

EC8. An incidental test expects removed prose; the test migrates while the governing semantic rule remains.

EC9. Common-path size shrinks but universal materiality policy moves behind a reference; semantic review fails acceptance.

EC10. Automation authorization is stale or belongs to another change; automated mode is invalid.

## Non-goals

- Changing proposal lifecycle, formal-review recording schemas, change metadata, workflow continuation, correction authority, or downstream stage ownership.
- Creating a generic review engine, cross-skill policy owner, runtime router, scheduler, selector, cache, or state store.
- Adding another output asset or fragmenting the two coherent conditional procedures.
- Executing or grading Codex, Claude Code, opencode, or another target-agent runtime for acceptance.
- Adding permanent size, prose-quality, tokenizer, semantic-classifier, or scenario-framework validators.
- Optimizing another skill in this change.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-PRRSIM-001 | Every invocation resolves valid recording and automation modes or stops before side effects. |
| AC-PRRSIM-002 | Durable recording activates exhaustively, including late material and non-approval outcomes. |
| AC-PRRSIM-003 | Advisory recording, formal settlement, automation, correction, and workflow continuation retain separate authority. |
| AC-PRRSIM-004 | Required recording follows the governing change-ID order and safe generated roots grant no lifecycle authority. |
| AC-PRRSIM-005 | Specialized predicates are closed, review-owned, composable, late-loadable, and fail closed on ambiguity. |
| AC-PRRSIM-006 | Exactly four resource assemblies load the two conditional references independently. |
| AC-PRRSIM-007 | Missing triggered resources stop before dependent behavior and are never reconstructed. |
| AC-PRRSIM-008 | The existing assets remain the sole structural owners and apply one core plus four conditional result groups. |
| AC-PRRSIM-009 | Every semantic rule and literal dependency has one valid disposition and destination. |
| AC-PRRSIM-010 | Static proof covers valid and invalid modes, recording roots, authority, predicates, groups, failure, and parity. |
| AC-PRRSIM-011 | Acceptance executes no target-agent runtime and introduces no permanent simplicity machinery. |
| AC-PRRSIM-012 | Measurements report common-path, assembly, resource, and total-package words and bytes separately. |
| AC-PRRSIM-013 | Canonical, generated, packed, and installed packages preserve every mapped resource and required raw-byte parity. |
| AC-PRRSIM-014 | Existing proposal judgment, recording, settlement, isolation, status, claim, and handoff semantics remain intact. |
| AC-PRRSIM-015 | Architecture applicability is recorded before planning and any required architecture change is owned by this change. |
| AC-PRRSIM-016 | Rollout and rollback are atomic complete-package operations. |

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
The specification closes package shape, modes, authority, recording, specialized gates, output ownership, failure handling, compatibility, measurement, and proof without authorizing implementation.
