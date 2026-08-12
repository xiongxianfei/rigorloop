# Spec-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-12-spec-review-skill-simplification.md`

## Goal and context

Simplify the published `spec-review` package so isolated formal review loads a compact, self-sufficient review and recording contract, while governed settlement and workflow-managed automation load one conditional procedure.

The change preserves review rigor, durable recording, status and finding semantics, boundary-first activation, lifecycle ownership, and package parity. It changes instruction placement and resource loading, not review outcomes, workflow order, recording schema, or mutation authority.

## Glossary

- `formal review`: every invocation owned by `spec-review`; informal critique without a formal result is outside this skill.
- `settlement mode`: exactly `isolated` or `governed-spec-entry`.
- `automation mode`: exactly `manual` or `workflow-managed-automated`.
- `governed reference`: `references/governed-spec-review-settlement.md`, which owns only governed settlement and automation procedure.
- `boundary procedure`: the existing checked-revision activation and its projected compact-core and feature-authoring references.
- `recording-only root`: a minimal formal-review evidence root that does not establish governed lifecycle authority.
- `resource profile`: one of `SR1-isolated-formal`, `SR1B-isolated-formal-boundary`, `SR2-governed-formal`, or `SR2B-governed-formal-boundary`.

## Examples first

### Example E1: isolated clean review stays on the common path

Given a direct `spec-review` has no same-change governed settlement authority
When the review approves the specification without material findings
Then it loads `SR1-isolated-formal`, creates the required clean receipt and review-log entry from inline procedure, and performs no lifecycle settlement or workflow continuation.

### Example E2: an isolated material result remains durable

Given an isolated formal review produces a material finding
When the review completes
Then it records the detailed review, review log, and required resolution evidence without loading governed settlement procedure or creating governed authority.

### Example E3: governed manual review loads settlement procedure

Given current evidence resolves the exact same change, specification, and reviewable spec entry
When workflow invokes manual `spec-review`
Then `SR2-governed-formal` loads the governed reference after classification and may settle only that matching spec entry after recording succeeds.

### Example E4: automation is an authority branch, not another package

Given current durable workflow authorization matches the governed change and spec entry
When automated formal review runs
Then it uses the same `SR2` resource assembly, adds automation evidence and pause behavior, and returns continuation control to workflow.

### Example E5: informal critique is not a hidden review profile

Given a user explicitly asks for discussion or critique without status, approval, readiness, durable review evidence, or lifecycle use
When the request is classified
Then it routes outside `spec-review` and emits no formal review status or record.

### Example E6: boundary procedure remains independently additive

Given checked-revision evidence requires active boundary interpretation
When an isolated or governed formal review runs
Then the compact-core reference loads, followed by feature-authoring guidance only when its existing trigger applies.

### Example E7: missing governed procedure fails after recording

Given universal review judgment and durable recording complete successfully
When governed settlement is required but its mapped reference is missing or unreadable
Then settlement and automation stop, the recorded review remains valid, and the skill does not reconstruct missing procedure from memory.

### Example E8: size reduction cannot hide semantic loss

Given the rewritten main file is shorter
When preservation evidence is evaluated
Then acceptance still fails unless isolated loaded words and bytes decrease, every significant rule and literal has a disposition, duplicate clusters have one loaded owner, and semantic review passes.

## Requirements

R1. The canonical published package MUST remain owned by `skills/spec-review/` and MUST contain `SKILL.md`, `references/governed-spec-review-settlement.md`, the two existing boundary references, `assets/review-result-skeleton.md`, and `assets/material-finding.md`.

R2. `SKILL.md` MUST be self-sufficient for isolated formal review judgment, durable recording, safe result reporting, and routing without loading the governed reference.

R3. Every invocation owned by `spec-review` MUST be formal and MUST create or update required durable review evidence or report blocked recording.

R4. Feedback, critique, or discussion explicitly requesting no formal status, approval, readiness, durable record, or lifecycle evidence MUST route outside `spec-review` and MUST NOT create a formal result profile.

R5. Ambiguous or conflicting evidence about whether a formal result is requested MUST stop before status selection or durable recording rather than silently classifying the request as informal.

R6. Settlement mode MUST be exactly `isolated` or `governed-spec-entry`; unknown, missing, stale, contradictory, or ambiguous settlement evidence MUST fail closed before governed mutation.

R7. `governed-spec-entry` MUST require current evidence that resolves exactly one governed change, the reviewed specification, and the matching reviewable spec entry.

R8. Direct wording, a material finding, an explicit durable-record request, or creation of a recording-only root MUST NOT establish governed settlement authority.

R9. Automation mode MUST be exactly `manual` or `workflow-managed-automated`; `workflow-managed-automated` MUST require current durable authorization for the same governed change and spec entry and MUST imply `governed-spec-entry`.

R10. Conversational wording, stale authorization, mismatched identity, or a recording-only root MUST NOT establish workflow-managed automation.

R11. Resource assembly MUST use exactly four profiles: `SR1-isolated-formal`, `SR1B-isolated-formal-boundary`, `SR2-governed-formal`, and `SR2B-governed-formal-boundary`.

R12. `SR1-isolated-formal` MUST load `SKILL.md` and the result asset, plus the finding asset only when used; it MUST NOT load the governed reference.

R13. `SR1B-isolated-formal-boundary` MUST add only the boundary resources required by the existing checked activation contract to the isolated profile.

R14. `SR2-governed-formal` MUST add the governed reference to the isolated profile only after `governed-spec-entry` authority is established.

R15. `SR2B-governed-formal-boundary` MUST add both the governed reference and applicable boundary resources, loading each unique resource once in the documented order.

R16. Automation MUST remain a procedure branch inside `SR2` and `SR2B`; it MUST NOT create a fifth loaded-resource profile or grant authority through resource availability.

R17. `SKILL.md` MUST retain purpose, trigger, near-miss routing, review-only edit restriction, target identity, evidence precedence, bounded reading, review dimensions and table structure, verdicts, severity, material-finding sufficiency, status and readiness vocabularies, universal stops, claims, handoff limits, resource triggers, and result applicability.

R18. `SKILL.md` MUST retain concise executable recording procedure covering portable location selection, clean receipt versus detailed record, review-log synchronization, conditional review-resolution, collision and retry behavior, blocked recording, and the rule that recording does not grant settlement.

R19. The inline recording procedure MUST preserve the behavior required by `specs/formal-review-recording.md` without copying its full change-ID algorithm, schema, or example set into shipped prose.

R20. Isolated recording MUST use the existing formal-review location order and MUST permit only the review record or clean receipt, `review-log.md`, conditional `review-resolution.md`, and minimal recording-only metadata required by the existing contract.

R21. A recording-only root MUST NOT create or mutate governed spec-entry settlement, active plan state, workflow routing, lifecycle progression, automation authorization, or automation run state.

R22. When no safe recording location can be selected or written, the review MAY return its judgment but MUST report `Recording status: blocked`, identify the blocker and smallest next action, and MUST NOT claim formal review completion, settlement, or continuation.

R23. The governed reference MUST load exactly for `governed-spec-entry` and MUST own only complete change-record inspection, matching spec-entry settlement, governed retries and conflicts, workflow-managed context reset and manifest evidence, automation pause behavior, and return-to-workflow procedure.

R24. The governed reference MUST NOT own universal recording, review judgment, status meaning, severity, materiality, boundary activation, stage order, workflow continuation, or permission to edit the reviewed specification.

R25. Governed settlement MUST occur only after universal recording succeeds and MUST mutate only the exact matching spec entry under existing review-peer authority; workflow MUST retain downstream routing and continuation ownership.

R26. The existing checked-revision boundary contract and `specs/boundary-first-resources.yaml` MUST remain the sole boundary activation and projection owners; this change MUST NOT alter boundary identifiers, paths, raw bytes, activation grammar, or grandfathering behavior.

R27. The inline four-question boundary scan MUST remain; when checked activation requires boundary procedure, the compact-core reference MUST load first and feature-authoring guidance MUST load only for formal boundary-record completeness or potentially substantive grandfathered revision.

R28. Unknown substantive-revision classification or a missing required boundary resource MUST block the dependent boundary conclusion and approval; a non-substantive grandfathered revision MUST NOT trigger formal record adoption.

R29. The existing result asset MUST remain the sole overall result structure and MUST contain one formal core, one recording group required for every review, and governed-settlement, boundary-review, and automated-review conditional groups.

R30. Inapplicable result groups MUST be omitted; applicable groups with unavailable required data MUST report explicit `blocked` or `unknown` state and blocker; unfilled placeholders MUST be forbidden.

R31. Assets MUST own only headings, labels, ordering, tables, placeholders, and short fill hints; they MUST NOT decide applicability, status, severity, recording, settlement, automation, or handoff policy.

R32. A missing, unreadable, contradictory, or mixed-version triggered resource MUST stop dependent interpretation or mutation; an untriggered resource MUST not load or block, and memory-based reconstruction MUST be forbidden.

R33. A change-local semantic rule-disposition ledger MUST inventory every behaviorally significant current rule with stable ID, source locations, behavior, governing requirements, applicable profiles, exactly one disposition, destination, and preservation proof.

R34. Semantic dispositions MUST be exactly `retained-inline`, `retained-governed-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; unknown or missing values MUST fail closed before consistency checks.

R35. A separate literal-compatibility inventory MUST record each exact dependency, source, consumers, required semantics, classification, disposition, and replacement.

R36. Literal classifications MUST be exactly `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`; normative literals MUST remain exact unless their contract changes, parser/package literals MUST migrate atomically, incidental tests MUST not own prose, and obsolete literals MUST have removal evidence.

R37. Profile measurement MUST use LF-normalized canonical files, count each unique loaded resource once in documented load order, and report UTF-8 bytes and Unicode whitespace-separated words for `SKILL.md`, every reference and asset, all four profiles, manual and automated governed evaluations, and the total package.

R38. Acceptance MUST require lower loaded words and bytes for `SR1-isolated-formal`, one loaded owner per duplicate cluster, complete rule and literal disposition, no unexplained governed-profile growth, honest total-package accounting, and preserved semantic and lifecycle behavior.

R39. A 25–40 percent `SKILL.md` reduction MUST remain a planning target rather than a normative threshold, and no size target may override safety, clarity, recording, or semantic preservation.

R40. Acceptance MUST use deterministic structural checks, static contract fixtures, existing package-chain validation, and independent semantic review; it MUST NOT execute a target-agent runtime, grade transcripts, add prompt journeys, introduce a tokenizer dependency, or create a permanent simplicity validator family.

R41. Existing validation owners MUST prove normalized structure, closed vocabularies, resource-map syntax, mapped-resource existence and containment, placeholder absence, boundary projection identity, and canonical/generated/packed/installed package parity.

R42. The simplification MUST preserve current verdicts, severity, material-finding requirements, review dimensions, evidence authority, recording, settlement, boundary-first behavior, readiness, stops, claims, lifecycle ownership, and handoff behavior except for the approved resource-loading and ownership changes.

R43. A bounded architecture assessment MUST precede planning and MUST select `architecture-not-required` when the established published-package model remains accurate; if implementation requires a package-model or independently governed-resource change, this change MUST own the required architecture artifact and review before planning.

R44. Rollout and rollback MUST update or restore the complete canonical package and directly coupled contract consumers atomically, regenerate derived packages, and fail partial or mixed package versions.

R45. `SFA-R6` remains satisfied by keeping recording obligations and lifecycle boundaries inline; conditional operational mechanics MAY live in the governed reference only as constrained by R18 through R25.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1-R45

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R3-R10 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R6-R10, R20-R25, R32, R43-R44 | BND-STATE-001 | - |
| identity-authority | applicable | R6-R10, R20-R25 | BND-AUTH-001 | - |
| composition-path | applicable | R1-R2, R11-R19, R23-R32, R41-R42 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R18-R25, R32, R44 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R5-R10, R22, R28, R32-R40, R43-R44 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R26-R28, R33-R45 | BND-COMPAT-001 | - |
| external-environment | applicable | R32, R37, R40-R41, R44 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R3-R10 | formal or outside-skill request; isolated or governed settlement; manual or automated execution; valid, stale, mismatched, or ambiguous evidence | every invocation has one valid classification before dependent work | valid profile or fail-closed routing result | R6 |
| BND-STATE-001 | state-lifecycle | R6-R10, R20-R25, R32, R43-R44 | recorded/blocked; isolated/governed; manual/automated; complete/missing resource; assessed/ambiguous architecture | recording precedes settlement; resources never grant authority | bounded write, safe stop, or atomic rollback | R25 |
| BND-AUTH-001 | identity-authority | R6-R10, R20-R25 | caller, review peer, governed spec entry, workflow authorization, workflow continuation owner | isolated evidence never becomes governed authority | permitted exact-entry mutation or authority blocker | R8 |
| BND-COMPOSE-001 | composition-path | R1-R2, R11-R19, R23-R32, R41-R42 | SR1, SR1B, SR2, SR2B; main file, governed reference, boundary resources, assets, derived packages | each rule and structure has one owner; each resource loads once | exact package assembly with preserved behavior | R11 |
| BND-TEMPORAL-001 | temporal-retry | R18-R25, R32, R44 | first recording, retry, conflict, stale authority, partial rollout, rollback | retries re-read current evidence and preserve first-pass review identity | idempotent completion, explicit conflict, or stop | R18 |
| BND-RECOVERY-001 | failure-recovery | R5-R10, R22, R28, R32-R40, R43-R44 | ambiguity, blocked recording, missing resource, invalid vocabulary, unsafe reduction, architecture ambiguity | failure never invents authority, procedure, or semantic deletion | owner-routed correction, blocker, or rollback | R32 |
| BND-COMPAT-001 | compatibility-migration | R26-R28, R33-R45 | retained, moved, duplicate, obsolete rules; normative, parser, incidental, obsolete literals; old/current package | significant rules never disappear and projected resources do not drift | compatible current package or complete rollback | R42 |
| BND-ENV-001 | external-environment | R32, R37, R40-R41, R44 | canonical, generated, packed, installed trees; runtime present or absent | acceptance is deterministic and filesystem/package based | parity proof or package-integrity failure | R40 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R6-R16 | BND-INPUT-001, BND-COMPOSE-001 | ambiguous authority could load governed procedure or automation | stop before governed loading or mutation |
| INT-002 | R18-R25 | BND-STATE-001, BND-AUTH-001 | durable recording could be mistaken for settlement authority | record successfully while preserving isolated mutation limits |
| INT-003 | R23-R25, R32 | BND-COMPOSE-001, BND-RECOVERY-001 | missing governed resource after recording could erase or overstate review outcome | preserve the record and stop only dependent settlement and automation |
| INT-004 | R26-R28, R32 | BND-COMPOSE-001, BND-COMPAT-001 | local simplification could diverge from checked boundary activation or projected bytes | consume the existing decision and preserve projection identity |
| INT-005 | R33-R40, R42 | BND-RECOVERY-001, BND-COMPAT-001 | size pressure or incidental tests could remove governing behavior | closed ledgers and semantic review block unsafe reduction |
| INT-006 | R41, R44 | BND-COMPOSE-001, BND-ENV-001 | a generated or installed package could omit the new reference | package-chain parity fails before release or dependent runtime use |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R2, R3, R12, R18 | BND-COMPOSE-001 | - | - |
| E2 | illustration | R18-R22 | BND-STATE-001, BND-AUTH-001 | - | - |
| E3 | illustration | R7, R14, R23-R25 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E4 | illustration | R9, R16, R23-R25 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | illustration | R4-R5 | BND-INPUT-001 | - | - |
| E6 | illustration | R13, R15, R26-R28 | BND-COMPOSE-001, BND-COMPAT-001 | - | - |
| E7 | illustration | R22-R25, R32 | BND-COMPOSE-001, BND-RECOVERY-001 | - | - |
| E8 | illustration | R33-R40 | BND-RECOVERY-001, BND-COMPAT-001 | - | - |

## Inputs and outputs

Inputs are the formal review request, exact specification identity, current change and spec-entry evidence when governed settlement is requested, current workflow authorization when automation is requested, applicable checked boundary evidence, project-local instructions, the full reviewed specification, and relevant contracts and validation evidence.

Outputs use the existing result and finding assets. Every formal result includes review identity, target, status, findings or none, blockers, recording status and paths, immediate next stage, eventual test-spec readiness, stop condition, and claim limitations. Conditional groups add only evidence applicable to governed settlement, boundary review, or automation.

## State and invariants

- Every `spec-review` invocation is formal and requires recorded or explicitly blocked evidence.
- Resource loading and execution authority are separate.
- Universal recording succeeds or blocks before governed settlement.
- An isolated result never advances workflow state.
- Workflow-managed automation implies current exact same-change governed authority.
- Boundary activation and resource projection keep their existing owners.
- Assets are structural leaves and references remain owned by the `spec-review` package.
- Change-local ledgers and measurements are proof artifacts, not permanent product state.

## Error and boundary behavior

- Unknown classification values fail before consistency checks.
- Ambiguous review intent routes to a stop rather than an informal downgrade.
- Missing recording identity or failed write reports blocked recording and limits claims.
- Missing or contradictory governed resources preserve completed judgment and recording but block settlement and automation.
- Missing required boundary resources block the dependent boundary conclusion and approval.
- Stale or mismatched workflow authorization blocks automation.
- Mixed package versions block dependent use and release validation.

## Compatibility and migration

Current review status values, severity, finding fields, recording artifacts, lifecycle meanings, boundary identifiers, result labels, and handoff semantics remain compatible. No user-data or `change.yaml` schema migration is introduced.

Canonical skill content, the new reference, coupled spec/test consumers, and derived package inventories roll out atomically. Rollback restores the prior complete package and consumers, regenerates derived outputs, and revalidates package parity.

## Observability

Implementation evidence records rule disposition, literal compatibility, duplicate ownership, before/after resource and profile measurements, static scenario results, package-chain parity, and independent semantic review. Validation evidence names exact commands and outcomes. Target-agent transcripts and runtime behavior are not acceptance evidence.

## Security and privacy

The change adds no network access, credentials, secrets, external mutation, or user-data processing. Resource containment and exact identity checks prevent path escape and mixed-package behavior.

## Accessibility and UX

No graphical interface changes. The shorter isolated profile improves scanability, while closed classifications and explicit blockers preserve usability for review authors and maintainers.

## Performance expectations

`SR1-isolated-formal` loaded words and UTF-8 bytes must decrease from baseline. The 25–40 percent main-file target is advisory. No runtime latency, model-token, or target-agent performance guarantee is introduced.

## Edge cases

EC1. A direct review has an existing change root but no matching governed spec entry; it remains isolated and may record there without settling it.

EC2. A material finding creates a recording-only root; the root does not activate workflow or automation.

EC3. Recording succeeds but the governed reference is absent; the review remains recorded while settlement is blocked.

EC4. The governed reference exists but authorization names another spec entry; settlement and automation stop.

EC5. Boundary activation is discovered late; required references load in order before the boundary verdict and final review status.

EC6. A grandfathered revision cannot be classified as substantive or non-substantive; approval stops for owner resolution.

EC7. An asset group is applicable but a required path is unavailable; the group reports blocked state rather than an empty placeholder.

EC8. A parser consumes an exact current heading; implementation preserves it or migrates the parser and every consumer atomically.

EC9. The main file shrinks but the isolated profile does not; simplification acceptance fails.

EC10. Total package size grows because of the new reference; the change may proceed only with separate reported justification and preserved isolated-profile reduction.

## Non-goals

- Changing review judgment, workflow order, lifecycle schema, boundary activation, recording schema, or downstream ownership.
- Optimizing another skill.
- Creating a generic review engine, runtime router, state store, or new validator family.
- Executing or grading target-agent runtimes.
- Adding another output asset, tokenizer dependency, or permanent size gate.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every formal invocation maps to exactly one settlement mode, automation mode, and resource profile or fails closed. |
| AC2 | Isolated formal review performs complete durable recording without loading the governed reference. |
| AC3 | Governed settlement and automation require exact current same-change authority and never arise from resource loading. |
| AC4 | Universal judgment, recording, stops, claims, and handoff limits remain inline and semantically preserved. |
| AC5 | Existing boundary activation, load order, grandfathering, paths, and projected bytes remain unchanged. |
| AC6 | The existing result and finding assets remain structural, omit inapplicable groups, and contain no unfilled placeholders. |
| AC7 | Missing required resources stop only the dependent procedure without remembered reconstruction or false completion claims. |
| AC8 | Every significant rule, literal dependency, and duplicate cluster has one classified disposition and owner. |
| AC9 | `SR1-isolated-formal` loaded words and bytes decrease; governed and total-package deltas are reported separately and justified. |
| AC10 | Deterministic fixtures and existing validators prove structure, closed vocabularies, failure behavior, and package parity without target-agent execution. |
| AC11 | A bounded architecture assessment is recorded before planning and any required architecture change is owned by this change. |
| AC12 | Rollout and rollback operate on complete package revisions and reject mixed versions. |

## Open questions

None.

## Next artifacts

- Formal `spec-review` evidence and settlement.
- Bounded architecture assessment.
- Execution plan and `plan-review`.
- Test specification and `test-spec-review`.

## Follow-on artifacts

None yet.

## Readiness

Ready for formal `spec-review`. This artifact does not claim review approval, architecture disposition, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
