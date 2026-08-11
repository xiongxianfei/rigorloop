# Test-Spec-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-11-test-spec-review-skill-simplification.md`

## Goal and context

Simplify the published `test-spec-review` skill so ordinary advisory review loads a compact universal contract, while durable recording, formal settlement, and boundary-first proof procedure load only when their independent triggers apply.

The change preserves proof-map rigor, formal review evidence, isolated material-finding recording, closed status and handoff behavior, review independence, package integrity, and downstream authority.
It changes package composition and instruction ownership, not workflow stage order, review meanings, implementation eligibility, or runtime architecture.

## Glossary

- `lifecycle mode`: exactly `formal` or `advisory`; it determines whether the review may settle a governed test-spec artifact.
- `handoff mode`: exactly `isolated` or `workflow-managed`; it controls automatic continuation independently of lifecycle mode.
- `boundary-first context`: authoritative feature or proof evidence activates `boundary-first-v1` or makes its applicability materially undecidable.
- `durable recording context`: derived context that applies to every formal review, every material or blocking outcome, and every explicit durable-record request.
- `base assembly`: one of `TSR0-isolated`, `TSR0B-isolated-boundary`, `TSR1-formal`, or `TSR1B-formal-boundary`.
- `recording overlay`: `references/test-spec-review-recording-and-settlement.md` plus `assets/review-result-skeleton.md`, with `assets/material-finding.md` added once per material finding.
- `formal-only settlement`: the recording-reference subsection that may settle exactly one governed test-spec artifact entry and may run only in formal lifecycle mode.
- `universal proof semantics`: proof-adequacy, negative-case, command, fixture, manual-proof, staleness, status, finding, stop, claim, and handoff rules required by every review.

## Examples first

### Example E1: clean advisory review stays on the common path

Given a direct advisory proof-map review has no boundary-first trigger and produces no material or blocking outcome
When review completes
Then it loads only `SKILL.md`, returns an isolated result, creates no durable lifecycle record unless explicitly requested, and does not authorize implementation.

### Example E2: isolated material finding triggers recording

Given a non-formal isolated review begins without the recording overlay
When it discovers a material proof-map defect
Then `durable_recording_context` becomes true, the recording overlay loads before final output, the finding is recorded or recording is reported blocked, and downstream handoff remains stopped.

### Example E3: formal review can remain isolated

Given a direct invocation is a valid formal lifecycle review but has no workflow-managed continuation authority
When the review produces an approved result
Then it records and settles the matching test-spec artifact, reports `Implementation handoff: allowed`, and does not automatically invoke implementation.

### Example E4: workflow-managed formal approval may be routed

Given current automation authority selects a valid formal review for the same change
When the review is recorded as `approved` with no open finding or stale test-spec revision
Then the review settles only its artifact and returns control to workflow, which may route from the closed status mapping.

### Example E5: explicit recording does not create formal authority

Given a clean advisory review explicitly requests a durable record
When recording completes
Then the recording overlay is used, but the formal-only settlement subsection does not run and implementation handoff remains isolated.

### Example E6: boundary-first loading is independently additive

Given the governing feature uses `boundary-first-v1` or proof applicability is materially undecidable
When the test spec is reviewed
Then both existing boundary-first references load once in documented order in addition to the applicable ordinary or formal base assembly.

### Example E7: a missing required recording resource fails safely

Given an isolated material finding requires durable recording
When the recording reference or required asset is missing or unreadable
Then the finding remains visible, `Recording status: blocked` names the expected path and smallest corrective action, and no downstream handoff occurs.

### Example E8: an ordinary review does not load boundary procedure

Given authoritative requirements and the proof map establish that `boundary-first-v1` is not applicable
When review begins
Then neither boundary-first reference loads and universal proof semantics remain sufficient for the review.

### Example E9: advisory review cannot receive workflow-managed handoff

Given lifecycle mode resolves `advisory` while current handoff evidence requests `workflow-managed`
When invocation validity is checked
Then review stops before proof judgment, recording, settlement, or downstream routing and identifies that workflow-managed continuation requires formal review context.

## Requirements

R1. The complete authored `test-spec-review` package MUST remain owned by `skills/test-spec-review/` and MUST contain canonical `SKILL.md`, `references/test-spec-review-recording-and-settlement.md`, both existing boundary-first references, and both existing structural assets.

R2. `SKILL.md` MUST remain self-sufficient for every valid advisory review, including purpose, routing, input authority, lifecycle and handoff classification, boundary applicability, the durable-recording trigger, universal proof semantics, findings, closed outcomes, stops, claims, and bounded handoff.

R3. Lifecycle mode MUST be exactly `formal` or `advisory`, and handoff mode MUST be exactly `isolated` or `workflow-managed`; the two classifications MUST be independent, and a formal review MAY have isolated handoff.

R4. `formal` lifecycle mode MUST resolve exactly one active test-spec artifact, its owning `stage-owned-change-local-v1` change record, current authoring evidence, and a lifecycle state requiring `test-spec-review`; missing, stale, contradictory, mismatched, or ambiguous evidence MUST stop before formal settlement.

R5. `isolated` handoff mode MUST apply to direct or review-only invocation or missing current workflow continuation authority and MUST prevent automatic downstream invocation even when formal settlement or `Implementation handoff: allowed` is recorded.

R6. `boundary-first context` MUST be determined from governing feature and proof evidence, not conversational wording or the mere textual presence or absence of stable IDs; materially undecidable applicability MUST stop or produce a material upstream gap.

R7. `durable recording context` MUST become true for every formal review, every material finding, every blocking review outcome, and every explicit durable-record request.

R8. A formal review MUST load the recording overlay before review settlement; an advisory clean review MUST NOT load it unless recording was explicitly requested; an advisory material or blocking review MUST load it as soon as the outcome is known and before final output.

R9. Base assembly MUST be exactly `TSR0-isolated` (`SKILL.md`), `TSR0B-isolated-boundary` (`SKILL.md` plus both boundary references), `TSR1-formal` (`SKILL.md` plus recording overlay), or `TSR1B-formal-boundary` (`SKILL.md`, both boundary references, and recording overlay).

R10. The recording overlay MUST consist of the recording-and-settlement reference plus the result asset, with the material-finding asset copied exactly once per material finding and no empty finding block for a no-material result.

R11. Loading the recording overlay after an advisory review begins MUST change only recording obligations; it MUST NOT change lifecycle mode, handoff mode, review status meaning, or implementation authority.

R12. The recording reference MUST visibly separate shared recording procedure from formal-only settlement procedure, and advisory lifecycle mode MUST NOT execute the formal-only subsection.

R13. Shared recording procedure MUST own record-root resolution or creation, detailed records and clean receipts when applicable, review-log registration, review-resolution creation when material findings or another approved disposition trigger applies, asset use, blocked-recording diagnostics, and retry or conflict handling.

R14. Formal-only settlement MUST validate the current test-spec entry and authoring evidence, write the durable review record before settlement, remove authoring evidence, write the exact review mapping, and settle only the matching test-spec artifact entry without mutating workflow routing.

R15. Every isolated material finding MUST be recorded in the required change-local review files before review-driven fixes, or the output MUST report `Recording status: blocked`, the required record path, record-before-fixing or reconstruction status, owner-decision status, and the smallest corrective action.

R16. A blocking or revision outcome MUST use a detailed record and MUST create or update `review-resolution.md` when disposition is required; a clean no-material review MUST NOT create an empty finding block or require empty review resolution solely because it was recorded.

R17. The result and finding assets MUST own labels and layout only; `SKILL.md` and the applicable reference MUST own applicability, status meaning, materiality, recording, settlement, claims, and handoff policy.

R18. Missing, unreadable, contradictory, escaped, or mixed-version required resources MUST stop dependent work or report blocked recording as applicable; untriggered resources MUST NOT load or block review; memory-based reconstruction MUST be forbidden.

R19. Universal proof semantics MUST preserve requirement and acceptance-criterion traceability, negative and failure coverage, milestone mapping, command ownership and classification, deterministic fixtures, complete manual-proof fields, and stale or insufficient evidence behavior.

R20. Review status MUST remain exactly `approved`, `changes-requested`, `blocked`, or `inconclusive`; immediate next stage MUST remain exactly `test-spec revision`, `spec revision`, `architecture revision`, `plan revision`, `review-resolution`, `implement`, or `none`; implementation handoff MUST remain exactly `allowed` or `not-allowed`.

R21. `approved` MUST map to `implement` and `allowed`; every other status MUST map to `not-allowed`, with `changes-requested`, `blocked`, and `inconclusive` retaining their current routing and evidence meanings.

R22. Formal and advisory review MUST use the same proof-quality, materiality, status, stop, staleness, claim, and output semantics; advisory approval MUST NOT satisfy formal implementation eligibility.

R23. An approved formal review MUST become stale after a substantive test-spec change and MUST remain current after a confirmed non-substantive formatting-only change under the existing staleness contract.

R24. The refactor MUST preserve review independence, including first-pass finding recording before review-driven fixes and the prohibition on rewriting the test spec during review unless a combined review-and-revision action is explicitly authorized.

R25. A change-local semantic rule-disposition ledger MUST inventory every behaviorally significant current rule with stable ID, source locations, behavior, governing requirements, applicable assemblies, one closed disposition, destination, and preservation proof.

R26. Semantic dispositions MUST be exactly `retained-inline`, `retained-recording-reference`, `retained-boundary-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; missing or unknown values MUST fail closed before consistency checks.

R27. A separate change-local literal-compatibility inventory MUST record literal, source, consumers, required semantics, disposition, and replacement and MUST classify each dependency exactly as `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, or `obsolete`.

R28. Normative literals MUST remain exact unless the governing contract changes; parser or package literals MUST migrate with every consumer; incidental test wording MUST be updated rather than promoted to policy; obsolete literals MUST have removal evidence.

R29. Assembly measurement MUST use canonical LF-normalized resources, count each unique resource once in documented load order, and report UTF-8 bytes and Unicode whitespace-separated words for `SKILL.md`, every resource, each base assembly and recording overlay, and the total package.

R30. The 30-40 percent `SKILL.md` reduction MUST remain advisory; acceptance MUST require complete rule disposition, one owner for each duplicate cluster, material ordinary-path reduction, separate total-package accounting, and no behavioral loss.

R31. Acceptance MUST use deterministic structural validation, static contract fixtures, existing package-chain proof, and independent semantic review and MUST NOT execute or grade Codex, Claude Code, opencode, or another target-agent runtime.

R32. The change MUST NOT add prompt journeys, transcript grading, runtime certification, a permanent simplicity or prose-quality validator, or a new tokenizer dependency.

R33. Existing validation owners MUST prove normalized skill structure, closed vocabulary failure, exact resource-map triggers, resource existence and containment, asset placeholder absence, canonical and derived package parity, and unchanged boundary-reference identity.

R34. The two existing boundary-first references MUST remain governed deterministic projections and MUST load together exactly when `boundary_first_context` is true.

R35. Repeated quick-guide, routing, stop, recording, finding, and output structures MUST have one policy or structural owner and MUST NOT be duplicated across inline text, references, and assets.

R36. A recorded architecture assessment MUST precede planning; it MUST select `architecture-not-required` when the existing packaged-skill model remains accurate and MUST route through architecture authoring and review when implementation changes that model or requires a current architecture correction.

R37. Rollout and rollback MUST operate on one complete canonical package revision and all coupled literal consumers; mixed or partial package versions MUST fail deterministic package validation and dependent procedure.

R38. The simplification MUST preserve existing proof review, recording, settlement, staleness, status, claims, outputs, handoff, workflow integration, and implementation-eligibility behavior except for the approved resource-loading and ownership changes.

R39. The lifecycle-by-handoff validity matrix MUST permit exactly `formal + isolated`, `formal + workflow-managed`, and `advisory + isolated`; `advisory + workflow-managed` MUST stop before review or downstream routing because workflow-managed continuation requires formal review identity and settlement authority.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R3, R4, R5, R6, R7, R9, R20, R39 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R3, R4, R5, R7, R8, R11, R12, R14, R15, R16, R18, R23, R36, R37, R39 | BND-STATE-001 | - |
| identity-authority | applicable | R3, R4, R5, R11, R12, R14, R15, R21, R22, R24, R39 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R8, R9, R10, R12, R13, R17, R18, R34, R35, R38 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R8, R13, R14, R15, R18, R23, R24, R37 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R4, R6, R15, R16, R18, R26, R27, R30, R31, R36, R37 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R20, R21, R23, R25, R26, R27, R28, R33, R35, R37, R38 | BND-COMPAT-001 | - |
| external-environment | applicable | R18, R29, R31, R32, R33, R34, R37 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R3, R4, R5, R6, R7, R9, R20, R39 | formal or advisory lifecycle; isolated or workflow-managed handoff; three valid pairs and one invalid pair; boundary applicable or not; recording false then true; valid and unknown closed values | each classification has one authoritative value and unknown or invalid pairs fail closed | one valid assembly and authority set, or stop | R39 |
| BND-STATE-001 | state-lifecycle | R3, R4, R5, R7, R8, R11, R12, R14, R15, R16, R18, R23, R36, R37, R39 | advisory start to material outcome; formal authoring to review settlement; valid and invalid lifecycle-handoff pair; current to stale; complete to missing resource; architecture assessed or ambiguous | recording trigger may change without changing lifecycle or handoff authority; workflow-managed handoff requires formal lifecycle | recorded and correctly settled result, isolated blocker, or safe stop | R39 |
| BND-AUTH-001 | identity-authority | R3, R4, R5, R11, R12, R14, R15, R21, R22, R24, R39 | caller, formal reviewer, workflow, test-spec author, and implement authority; same or mismatched target; formal or advisory continuation basis | review records only owned evidence; workflow routes only from formal review; advisory result never establishes formal eligibility | bounded record and handoff, or authority stop | R39 |
| BND-COMPOSE-001 | composition-path | R1, R2, R8, R9, R10, R12, R13, R17, R18, R34, R35, R38 | TSR0, TSR0B, TSR1, TSR1B; late recording overlay; result and finding assets; canonical through installed packages | universal policy stays inline; conditional procedure and structural layouts each have one owner | exact resource assembly and behavior-preserving result | R9 |
| BND-TEMPORAL-001 | temporal-retry | R8, R13, R14, R15, R18, R23, R24, R37 | pre-review formal load; post-outcome advisory load; record before fix; retry, stale evidence, partial package | material findings are durable before correction and stale approval never authorizes implementation | current record, deterministic retry, rereview, or blocker | R15 |
| BND-RECOVERY-001 | failure-recovery | R4, R6, R15, R16, R18, R26, R27, R30, R31, R36, R37 | ambiguous authority; missing resource; blocked recording; unknown ledger value; unsafe reduction; ambiguous architecture; rollback | failure never invents procedure, suppresses a finding, or permits handoff | owner correction, recorded blocker, or atomic rollback | R18 |
| BND-COMPAT-001 | compatibility-migration | R20, R21, R23, R25, R26, R27, R28, R33, R35, R37, R38 | current and prior vocabulary, literals, resources, packages, and review behavior | semantic rules never disappear and consumers migrate atomically | compatible current package or complete prior-package rollback | R28 |
| BND-ENV-001 | external-environment | R18, R29, R31, R32, R33, R34, R37 | canonical, generated, packed, and installed filesystems; target runtime present or absent | acceptance is deterministic and package based, never target-runtime based | parity proof, package failure, or safe runtime omission | R31 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R3, R5, R7, R8, R11, R14, R39 | BND-STATE-001, BND-AUTH-001 | formal settlement could be mistaken for workflow continuation, or advisory review could receive workflow-managed handoff | settlement records the review while isolated handoff still prevents automatic continuation; advisory plus workflow-managed stops |
| INT-002 | R7, R8, R10, R12, R13, R15, R17 | BND-STATE-001, BND-COMPOSE-001 | advisory material finding appears after the common path was selected | recording overlay loads before output, finding asset records each finding, and formal-only settlement stays disabled |
| INT-003 | R6, R9, R18, R34 | BND-INPUT-001, BND-COMPOSE-001 | conversational or textual cues could over- or under-load boundary guidance | authoritative applicability selects both boundary resources or stops as undecidable |
| INT-004 | R15, R16, R18 | BND-TEMPORAL-001, BND-RECOVERY-001 | missing recording resources could erase an isolated finding | preserve the finding, report blocked recording and corrective action, and prohibit handoff |
| INT-005 | R19, R20, R21, R22, R35, R38 | BND-COMPOSE-001, BND-COMPAT-001 | simplification could change verdict or handoff semantics | universal status and proof rules remain inline and parity fixtures preserve outcomes |
| INT-006 | R25, R26, R27, R28, R29, R30 | BND-RECOVERY-001, BND-COMPAT-001 | percentage pressure or incidental tests could remove policy | closed ledgers, semantic review, and advisory measurements preserve behavior |
| INT-007 | R31, R32, R33, R34, R37 | BND-COMPOSE-001, BND-ENV-001 | a derived package could omit or transform one required resource | existing package-chain checks prove complete path and byte parity without target-runtime execution |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R2, R8, R9 | BND-COMPOSE-001 | - | - |
| E2 | regression | R8 | BND-STATE-001, BND-COMPOSE-001 | TSRSIM-PR1 | - |
| E3 | illustration | R3, R5, R14, R21 | BND-AUTH-001 | - | - |
| E4 | illustration | R3, R5, R14 | BND-STATE-001, BND-AUTH-001 | - | - |
| E5 | illustration | R12 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E6 | illustration | R9 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E7 | regression | R15, R18 | BND-TEMPORAL-001, BND-RECOVERY-001 | TSRSIM-PR1 | - |
| E8 | illustration | R9 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E9 | illustration | R39 | BND-INPUT-001, BND-STATE-001, BND-AUTH-001 | - | - |

## Inputs and outputs

Inputs are the direct or workflow-managed request, lifecycle and handoff authority, the active test spec, accepted feature spec, architecture when applicable, active plan and clean plan review, current review history, authoritative boundary and proof records, command and fixture descriptions, manual-proof contracts, and package resources.

Every output identifies lifecycle mode, handoff mode, boundary applicability, recording applicability, loaded resources, review status, material finding IDs, recording status and paths, blockers, immediate next stage, implementation handoff, stop condition, and claim limitations.

## State and invariants

- Lifecycle mode, handoff mode, boundary applicability, and durable recording are separate classifications.
- The only valid lifecycle and handoff pairs are formal with either handoff mode and advisory with isolated handoff.
- Durable recording is derived and may change after an advisory review begins.
- Conditional procedure supplies mechanics but never grants authority.
- Formal settlement writes only the matching test-spec artifact entry after review evidence is durable.
- Isolation controls automatic continuation, not mandatory recording.
- Universal proof and status meanings remain available without a conditional resource.
- The complete published skill is `SKILL.md` plus explicitly mapped references and assets under one `test-spec-review` owner.
- Rule, literal, fixture, and measurement artifacts are change-local proof, not recurring runtime state.

## Error and boundary behavior

- Unknown lifecycle, handoff, status, stage, handoff, or ledger values fail before consistency checks.
- Ambiguous formal target identity stops before review settlement.
- Undecidable boundary applicability stops or records an upstream material gap.
- Missing recording procedure preserves the finding or blocker and returns blocked recording rather than a partial durable record.
- Missing boundary procedure stops the boundary-dependent verdict without affecting an unrelated ordinary review.
- A late recording trigger never upgrades advisory lifecycle or isolated handoff authority.
- Advisory lifecycle with workflow-managed handoff stops before review and cannot degrade silently to another mode.
- Stale approval and open findings cannot authorize implementation.

## Compatibility and migration

Existing review statuses, next-stage values, handoff values, finding fields, recording paths, staleness rules, review decisions, and implementation eligibility remain compatible.
The migration deduplicates prose and moves conditional procedure; it does not migrate user data or change `change.yaml` schema.

Canonical skill changes, mapped resources, exact literal consumers, generated packages, archives, and installed-package proof roll out atomically.
Rollback restores the complete prior canonical package and consumer set, then regenerates and revalidates derived packages.

## Observability

Implementation evidence records the semantic rule ledger, literal inventory, static scenario fixtures, baseline and after measurements, each loaded assembly, duplicate-cluster ownership, package-chain proof, and independent semantic review.
Review records expose exact status, finding IDs, recording status and paths, blocker, next stage, handoff, and stop condition.
No transcript, model identity, or target-runtime output is acceptance evidence.

## Security and privacy

The change introduces no network, credential, secret, user-data, or external-action requirement.
Optional review-time command checks remain bounded to no-side-effect resolvability, help text, or dry run without secrets or network access.
Path containment and package parity prevent references from escaping the skill root or disappearing in an installed package.

## Accessibility and UX

No graphical interface changes.
The shorter common path, closed vocabulary, compact classification, and exact blocker diagnostics improve instruction scanability without relying on color or tool-specific UI.

## Performance expectations

The ordinary `SKILL.md` path must be materially smaller than baseline without weakening semantic coverage.
The 30-40 percent reduction remains advisory, total package size is reported separately, and no runtime latency or target-specific token guarantee is introduced.

## Edge cases

EC1. A direct formal review is valid but has no continuation authority; it settles the test-spec entry and stops after reporting the handoff value.

EC2. An advisory review discovers two material findings after starting without recording procedure; it loads the overlay once and copies the finding asset twice.

EC3. An advisory clean review explicitly requests a durable record; it records without formal settlement or implementation eligibility.

EC4. A material finding is known but the finding asset is missing; recording is blocked, the finding remains visible in output, and no fix or handoff proceeds.

EC5. A formal clean review has a result asset but no recording reference; it stops before recording or settlement.

EC6. A proof map contains `PRF-*` text for a non-boundary feature; text alone does not activate boundary-first context.

EC7. Governing evidence activates boundary-first but one boundary reference is stale; the boundary-dependent verdict stops as a package-integrity failure.

EC8. A formatting-only test-spec edit is confirmed non-substantive; prior formal approval remains current under the existing staleness contract.

EC9. An unknown review status appears with an otherwise consistent handoff; validation rejects the unknown status before checking the combination.

EC10. `SKILL.md` shrinks but universal proof rules are duplicated in the new reference; semantic ownership review fails acceptance.

EC11. A target-agent runtime is unavailable; deterministic static and package proof remains sufficient for acceptance.

EC12. The architecture assessment finds a stale flat-package example; this change registers and owns the bounded architecture update before planning.

EC13. Current automation evidence requests workflow-managed continuation but formal test-spec-review identity is absent; invocation stops before review and names the missing formal authority.

## Non-goals

- Changing workflow stages, `change.yaml` schema, review outcome meanings, implementation eligibility, or workflow routing ownership.
- Weakening proof adequacy, negative coverage, command classification, fixture determinism, manual proof, staleness, or review independence.
- Giving advisory review formal settlement or automatic implementation authority.
- Giving structural assets policy ownership or changing the governed boundary resources.
- Building an executable reviewer, scheduler, selector, cache, state store, or target-agent harness.
- Adding permanent size, token, prose-quality, transcript, fixture-framework, or runtime-certification validators.
- Optimizing another skill or introducing a cross-review-family abstraction.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-TSRSIM-001 | Lifecycle mode and handoff mode are independently classified, including formal review with isolated handoff. |
| AC-TSRSIM-002 | Boundary applicability and durable-recording applicability use exact evidence and outcome triggers. |
| AC-TSRSIM-003 | Exactly four base assemblies and one recording overlay produce every valid resource combination. |
| AC-TSRSIM-004 | Advisory clean review stays on the common path unless recording is explicitly requested. |
| AC-TSRSIM-005 | Advisory material and blocking outcomes record before output or report complete blocked-recording evidence. |
| AC-TSRSIM-006 | Loading recording procedure never grants formal settlement or automatic handoff. |
| AC-TSRSIM-007 | Formal settlement writes only the matching test-spec entry after durable review evidence exists. |
| AC-TSRSIM-008 | Existing result and finding assets own structure only and emit no empty or unfilled blocks. |
| AC-TSRSIM-009 | Both existing boundary references load together only when authoritative applicability requires them. |
| AC-TSRSIM-010 | Missing triggered resources fail safely and are never reconstructed from memory. |
| AC-TSRSIM-011 | Universal proof, finding, status, staleness, stop, claim, and handoff rules remain inline and behaviorally unchanged. |
| AC-TSRSIM-012 | Every semantic rule and literal dependency has one valid classified disposition. |
| AC-TSRSIM-013 | Measurements report common path, each assembly, recording overlay, and total package words and bytes separately. |
| AC-TSRSIM-014 | Reduction percentages remain advisory and cannot override semantic preservation. |
| AC-TSRSIM-015 | Acceptance executes no target-agent runtime and introduces no permanent simplicity machinery. |
| AC-TSRSIM-016 | Canonical, generated, packed, archived, and installed packages preserve every mapped resource and required byte identity. |
| AC-TSRSIM-017 | Existing review, recording, settlement, workflow, claim, and implementation-eligibility behavior remains intact. |
| AC-TSRSIM-018 | Architecture applicability is recorded before planning, and rollout and rollback remain complete-package operations. |
| AC-TSRSIM-019 | The lifecycle-by-handoff matrix permits exactly three pairs and rejects advisory plus workflow-managed before review or routing. |

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
The specification closes the lifecycle, handoff, recording, boundary, resource, proof, preservation, compatibility, measurement, and package contracts without authorizing implementation.
