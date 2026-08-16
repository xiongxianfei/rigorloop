<!-- Template: spec-skeleton-v1 | Skill: spec | Template status: normative | Maintained alongside: skills/spec/SKILL.md | Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# Architecture Review Skill Simplification

## Owning change record

`docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

- [Architecture Review Skill Simplification](../docs/proposals/2026-08-16-architecture-review-skill-simplification.md)
- Approved [proposal-review R3](../docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/proposal-review-r3.md)

## Goal and context

This specification defines a shorter published `architecture-review` skill package without weakening architecture judgment, the accepted four review surfaces, formal recording, exact governed settlement, retry recovery, review independence, or workflow ownership.

The universal skill owns safe review classification and judgment. One conditional reference owns detailed canonical architecture and ADR review method, while a second conditional reference owns architecture-review-specific durable recording and settlement procedure. The shared isolation and recording subsection remains byte-identical inline, and no new output asset, runtime engine, target-agent acceptance system, lifecycle state, or independent write owner is introduced.

## Glossary

- `review subject`: the exact evidence set whose architecture consistency receives one semantic review status.
- `governing basis`: the decision-bearing specification, approving review, assessment receipt, accepted proposal or decision, architecture-method contract, and repository revision that authorize and constrain the judgment.
- `settlement target`: an existing governed canonical architecture or ADR entry that the review is authorized to transition.
- `target disposition`: the evidence-scoped result for one settlement target: approved or accepted, `revision-required`, `blocked`, or unchanged at `review-required`.
- `prepared settlement manifest`: existing formal-review evidence that records the complete intended target-state transaction before target mutation; it is not a new lifecycle state or independent authority.
- `review-occurrence blocker`: a blocker that prevents the review occurrence or its recording and therefore permits no target settlement.

## Examples first

### Example E1: record-only no-impact review

Given a formal no-impact review binds an exact architecture-assessment receipt and governing spec, when the rationale is approved, then durable review evidence is written and the settlement-target set remains empty.

### Example E2: package method disclosure

Given a canonical architecture package is under review, when the surface is classified, then the package-review reference loads before C4, arc42, diagram, or ADR judgment.

### Example E3: missing recording procedure

Given durable recording is required and the recording reference is unavailable, when review completes, then findings remain visible but formal completion and settlement are blocked.

### Example E4: changed governing basis

Given a prior approved judgment exists and the governing spec or architecture-assessment identity changes, when retry is requested, then a new review occurrence is required even if architecture bytes are unchanged.

### Example E5: one affected ADR

Given a combined package review is `changes-requested` because one ADR has a material gap, when settlement runs, then that ADR becomes `revision-required`, unaffected targets remain `review-required`, and no target is approved.

### Example E6: inconclusive review

Given required evidence is missing and the review is `inconclusive`, when formal evidence is recorded, then settlement performs no target transition by default and workflow pauses.

### Example E7: prepared settlement

Given a governed target set is eligible for settlement, when review evidence and findings are complete, then the full manifest becomes durable before the first target transition.

### Example E8: partial physical settlement

Given one exact target transition completed before interruption, when an identical retry runs, then it reconciles the same manifest and completes only pending matching writes without creating another semantic review.

### Example E9: concurrent target change

Given a target identity or pre-state changed after manifest preparation, when settlement or retry revalidates, then it stops without adopting the changed state.

### Example E10: advisory recording without a location

Given advisory durable recording is requested but no authorized standalone location resolves, when the review returns, then `recording_status` is `blocked` and no governed state is created.

### Example E11: shared literal preservation

Given the skill package is simplified, when canonical validation compares `## Isolation and Recording`, then its bytes match the shared normative projection exactly.

### Example E12: invalid authority combination

Given automation is paired with advisory recording or settlement is paired with non-formal recording, when classification runs, then it stops before any side effect.

## Requirements

### Package and universal ownership

R1. The canonical package MUST contain `skills/architecture-review/SKILL.md`, `references/architecture-package-review.md`, and `references/architecture-review-recording-and-settlement.md` and MUST add no structural asset in this change.

R2. `SKILL.md` MUST remain self-sufficient for purpose, review authority, target and revision resolution, the four review surfaces, evidence precedence, universal spec alignment, architecture-impact judgment, materiality, status, no-impact credibility, proposal/spec-gap routing, durable-recording classification, finding completeness, stops, claims, resource triggers, and compact result behavior.

R3. `architecture-package-review.md` MUST load for `canonical-architecture-update` and `ADR` surfaces and MUST own reviewer-specific C4, arc42, diagram, package-consistency, canonical-link, ADR-quality, and package-failure procedure.

R4. `architecture-review-recording-and-settlement.md` MUST load exactly when durable recording is required and MUST own architecture-review-specific record placement, log synchronization, conditional resolution, governed target settlement, prepared manifests, retry, concurrency, and workflow-managed automation procedure.

R5. Neither reference MUST own review-surface applicability, semantic status, materiality, shared isolation policy, workflow routing, or downstream continuation.

R6. The resource map MUST use `READ` with exact contained relative paths and closed positive triggers, and each reference MUST load at most once per invocation.

R7. A missing, unreadable, escaped, contradictory, stale, or mixed-version triggered reference MUST stop before its dependent judgment, recording, settlement, automation, or claim without remembered reconstruction.

### Shared recording compatibility

R8. `SKILL.md` MUST retain exactly one `## Isolation and Recording` subsection whose bytes match `templates/shared/review-isolation-and-recording.md` under the governing formal-review recording contract.

R9. The shared subsection MUST be classified as `normative-cross-skill-literal`, and the recording reference MUST NOT restate or paraphrase it.

R10. Any future shared-block change MUST amend the governing specification, shared projection, every consuming review skill, and deterministic parity checks atomically.

### Classification, loading, and authority

R11. Review surface MUST be exactly `canonical-architecture-update`, `ADR`, `no-architecture-impact-rationale`, or `proposal-or-spec-gap`.

R12. Recording mode MUST be exactly `none`, `advisory-durable`, or `formal-lifecycle`; artifact settlement MUST be exactly `none` or `exact-target-set`; and execution mode MUST be exactly `manual` or `workflow-managed-automated`.

R13. The only valid authority combinations MUST be `none/none/manual`, `advisory-durable/none/manual`, `formal-lifecycle/none/manual`, `formal-lifecycle/exact-target-set/manual`, `formal-lifecycle/none/workflow-managed-automated`, and `formal-lifecycle/exact-target-set/workflow-managed-automated`.

R14. Every unlisted, unknown, missing, mixed, or contradictory combination MUST stop before durable writes, settlement, automation evidence, or handoff.

R15. Durable recording MUST apply to every formal lifecycle review, explicit durable-record request, material finding, or review status `changes-requested`, `blocked`, or `inconclusive`.

R16. Loaded assemblies MUST be exactly `ARR0-core`, `ARR0M-method`, `ARR1-recorded`, and `ARR1M-recorded-method` according to package-method and durable-recording contexts.

R17. `advisory-durable` MUST write only to an explicit valid user path or project-local authorized standalone location and MUST NOT create a governed root, formal review log, review resolution, lifecycle entry, artifact settlement, automation evidence, or workflow continuation.

R18. When no advisory location resolves safely, the result MUST preserve the complete judgment and findings, set `recording_status: blocked`, and create no governed authority.

R19. Manual execution MUST remain isolated after any valid recording or settlement, while workflow-managed automated execution MUST return control to workflow without advancing routing itself.

### Review subject, basis, and targets

R20. Every formal review occurrence MUST bind separate `review_subject`, `governing_basis`, and optional ordered `settlement_targets` identities plus its review ID, round, record path, and review-log path.

R21. The governing basis MUST identify the governing specification and content identity, approving spec-review identity, applicable architecture-assessment receipt, accepted proposal or decision basis when relevant, architecture-method contract and identity, and repository revision.

R22. A canonical package subject MUST bind exact canonical Markdown, linked diagram sources, related reviewed ADRs, and governing basis; a standalone ADR subject MUST bind the exact ADR, current canonical linkage, and governing basis.

R23. A no-impact subject MUST bind the exact architecture-assessment receipt and proposal or specification basis, while a proposal/spec-gap subject MUST bind the exact upstream artifacts and architecture question or conflict.

R24. No-impact and proposal/spec-gap surfaces MUST have an empty settlement-target set and MUST NOT create or settle a rationale, architecture, or ADR lifecycle entry.

R25. A direct formal record-only invocation without one stable resolvable subject identity MUST report blocked recording or remain advisory and MUST NOT create an identity-free formal occurrence.

R26. Judgment reuse and identical retry MUST require an unchanged subject, governing basis, ordered target set, semantic status, review ID, and round.

R27. A changed specification, approving spec review, assessment receipt, accepted decision basis, architecture-method identity, repository revision, target identity, or target order MUST require a new review occurrence.

### Judgment and evidence-scoped target disposition

R28. One semantic review status, exactly `approved`, `changes-requested`, `blocked`, or `inconclusive`, MUST govern the complete review subject.

R29. Every material finding MUST identify affected settlement-target IDs when targets are affected, and every blocker MUST use exactly `review-occurrence`, `target-set`, or `target:<artifact-id>` scope.

R30. `approved` MUST transition every exact canonical architecture target to `approved` and every exact ADR target to the intended `accepted` or `active` state recorded by current authoring evidence; missing or ambiguous intended ADR state MUST block the complete settlement.

R31. `changes-requested` MUST transition only targets named by material findings to `revision-required` and MUST leave every unaffected target at `review-required`.

R32. A target-scoped `blocked` result MUST transition only the named target to `blocked`; a target-set blocker MAY transition all targets to `blocked` only when its evidence applies to the complete set; a review-occurrence blocker MUST perform no target settlement.

R33. `inconclusive` MUST perform no target settlement by default and MUST leave every target at `review-required` unless separate target-scoped blocker evidence justifies a blocked target.

R34. Recording failure, authority failure, stale identity, ambiguous target, or invalid lifecycle state MUST perform no target settlement.

R35. A non-approved occurrence MUST NOT approve any target or grant architecture-review downstream eligibility, and an unaffected target remaining `review-required` MUST NOT be represented as partial approval.

R36. Governed settlement MUST resolve only exact existing canonical architecture and ADR entries at `review-required` whose artifact ID, kind, normalized path, content identity, authoring-evidence identity, repository revision, and governing basis all match.

### Prepared settlement and recovery

R37. The durable review record, findings, review log, and required review resolution MUST be complete before settlement preparation.

R38. The complete prepared settlement manifest MUST be durable on the existing formal-review evidence surface before the first canonical architecture or ADR lifecycle transition.

R39. The manifest MUST bind a stable manifest ID and state, review ID and round, subject identity, governing-basis identity, ordered target identity, and for every target its artifact ID, kind, path, content identity, authoring-evidence identity, validated pre-state, disposition, expected post-state, and settlement progress.

R40. Manifest state MUST be exactly `prepared`, `partial`, `complete`, or `blocked` and MUST NOT become a lifecycle state or independent authority.

R41. Settlement MUST re-read the complete change record, authority, governing basis, and target identities after preparation and before compare-and-set writes in manifest order.

R42. Every target completion MUST be recorded or verified against the same manifest, and only a complete manifest MAY produce `settled` or downstream eligibility.

R43. An interruption after some exact writes MUST produce `partial-retry-required`, preserve one semantic judgment, and create no duplicate review, finding, log, or resolution evidence.

R44. Partial retry MUST reuse the exact review ID, round, semantic judgment, subject, governing basis, manifest, target order, target identities, authoring evidence, pre-states, dispositions, and expected post-states and MUST complete only pending matching writes.

R45. Changed identity, state, order, basis, authority, manifest, or concurrency evidence MUST block retry without adoption or unrelated mutation.

R46. Settlement and retry MUST preserve unrelated artifact entries, milestone state, workflow routing, reviewed artifact bytes, and every state surface not named by the exact manifest.

### Findings, output, preservation, and proof

R47. Architecture-review finding severity MUST remain `blocker`, `material`, or `minor`, and every finding MUST retain finding, location, severity, and recommendation fields.

R48. Material findings MUST additionally retain stable Finding ID, evidence, required outcome, and safe resolution path or `needs-decision` rationale.

R49. The compact result MUST distinguish review surface, review status, recording status, settlement result, review subject, governing basis, exact settlement targets, target dispositions, material findings, blockers, required canonical or ADR updates, next stage, and claim limitations.

R50. Every behaviorally significant current rule and duplicate cluster MUST receive one owner and disposition in a change-local semantic-rule ledger.

R51. Every compatibility-sensitive heading, label, enum, path, resource verb, shared literal, and consumed phrase MUST receive one classification and disposition in a separate literal-compatibility ledger.

R52. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST have an unknown-value regression test.

R53. Measurement MUST use canonical authored files, LF normalization, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded procedure once in `SKILL.md`, package-reference, recording-reference order.

R54. Measurement MUST report all four assemblies, each reference, the complete package, and total package growth separately; `ARR1-recorded` and `ARR1M-recorded-method` MUST decrease in words and bytes from baseline without semantic loss.

R55. Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode resources MUST retain required inventory and raw-byte parity through existing repository tooling.

R56. Acceptance MUST use deterministic contract, fixture, validator, lifecycle, package, and parity proof and MUST NOT execute a target-agent runtime, grade transcripts, add a prose classifier, add a tokenizer dependency, or add a separate manual semantic-review gate.

R57. Published skill text MUST remain project-portable and MUST keep repository-maintainer source, package, shared-projection, release, and validation mechanics in contributor or governing surfaces rather than the shipped procedure.

R58. If existing formal-review evidence cannot represent the complete governing basis, target dispositions, expected states, and per-target progress without a new schema, persistent transaction record, lifecycle state, or write owner, the bounded architecture assessment MUST return `architecture-required` before planning.

## Inputs and outputs

Inputs are the accepted proposal and reviews, current architecture-review skill, approved architecture method, formal-review recording contract, skill package contract, workflow contract, current validators and fixtures, package consumers, and governed change evidence when settlement applies.

Outputs are the simplified canonical skill, two references, directly coupled contract and fixture updates, semantic and literal ledgers, profile measurements, package parity evidence, and stage-owned lifecycle evidence.

## State and invariants

- `skills/` remains the sole authored skill source.
- Review applicability, semantic status, materiality, stops, and claims remain universal.
- Loading procedure never grants recording, settlement, automation, or routing authority.
- No-impact and proposal/spec-gap review remain evidence-only.
- One semantic status applies to the complete subject, and non-approved review grants no target approval.
- Prepared review evidence precedes target mutation and grants no independent authority.
- Architecture-review mutates only its review evidence and exact eligible target settlement state.
- Workflow remains the only routing owner.

## Error and boundary behavior

Every unknown vocabulary, invalid authority combination, unresolved subject, stale governing basis, unsafe advisory path, ambiguous target, missing authoring evidence, illegal lifecycle state, unavailable required reference, incomplete manifest, changed pre-state, concurrency conflict, parity defect, or unsafe retry fails closed with a concrete blocker. Failure before the first permitted target transition leaves lifecycle targets unchanged. Interrupted permitted work may resume only through the exact prepared manifest.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R11, R12, R13, R14, R16, R28, R29, R40 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R15, R19, R24, R25, R28, R30, R31, R32, R33, R34, R35, R36, R37, R38, R40, R41, R42, R43, R44, R45, R46 | BND-STATE-001 | - |
| identity-authority | applicable | R13, R14, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R29, R36, R39 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R16, R22, R23, R49, R50, R51, R55, R57 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R26, R27, R37, R38, R39, R40, R41, R42, R43, R44, R45 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R7, R14, R18, R25, R34, R37, R38, R41, R42, R43, R44, R45, R46, R58 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R8, R9, R10, R47, R48, R50, R51, R52, R53, R54, R55, R57 | BND-COMPAT-001 | - |
| external-environment | applicable | R7, R17, R18, R45, R55, R56 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R11, R12, R13, R14, R16, R28, R29, R40 | review surfaces, recording modes, settlement modes, execution modes, statuses, blocker scopes, and manifest states | unknown or invalid values fail before consistency checks | one valid classification proceeds; invalid input stops | R12 |
| BND-STATE-001 | state-lifecycle | R15, R19, R24, R25, R28, R30, R31, R32, R33, R34, R35, R36, R37, R38, R40, R41, R42, R43, R44, R45, R46 | non-formal, advisory, formal record-only, prepared, partially settled, complete, blocked, stale, or conflicting state | formal evidence precedes bounded target mutation and only complete approved review grants eligibility | valid work records or settles; unsupported state remains unchanged | R38 |
| BND-AUTH-001 | identity-authority | R13, R14, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R29, R36, R39 | advisory location, formal subject, governing basis, optional targets, exact review and retry identity | loading and semantic judgment do not grant mutation or routing | exact current authority permits bounded writes; ambiguity or staleness stops | R20 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R16, R22, R23, R49, R50, R51, R55, R57 | universal file, two conditional references, shared literal, canonical package, ADR, record-only subject, and generated packages | one owner per rule and every required resource is present and portable | valid composition loads once; missing, duplicated, or drifting composition stops | R1 |
| BND-TEMPORAL-001 | temporal-retry | R26, R27, R37, R38, R39, R40, R41, R42, R43, R44, R45 | first review, prepared settlement, partial write, exact retry, changed basis, changed target, or concurrent write | retry never silently rebinds judgment or intended writes | exact retry completes pending writes once; changed state stops | R44 |
| BND-RECOVERY-001 | failure-recovery | R7, R14, R18, R25, R34, R37, R38, R41, R42, R43, R44, R45, R46, R58 | blocked recording, blocked-before-write, safe partial, unsafe partial, missing evidence capability, or conflicting state | no target mutation occurs without complete durable intent and current authority | safe matching work reconciles; unsafe recovery or missing architecture support blocks | R38 |
| BND-COMPAT-001 | compatibility-migration | R8, R9, R10, R47, R48, R50, R51, R52, R53, R54, R55, R57 | normative shared literal, semantic rule, parser-sensitive literal, incidental prose, canonical source, or derived resource | shared bytes and package parity remain exact while ownership changes | classified atomic migration passes or blocks | R8 |
| BND-ENV-001 | external-environment | R7, R17, R18, R45, R55, R56 | valid local evidence path, unsafe path, unavailable resource, filesystem interruption, canonical package, or clean install | acceptance remains deterministic and repository-owned | local proof succeeds or dependent claim blocks | R56 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R13, R14, R17, R18, R19 | BND-INPUT-001, BND-AUTH-001, BND-ENV-001 | a known mode combination or missing advisory location silently grants formal or automated authority | only enumerated combinations and valid explicit locations permit their bounded side effects |
| INT-002 | R20, R21, R23, R24, R25, R26, R27 | BND-AUTH-001, BND-TEMPORAL-001 | artifact bytes remain unchanged while decision-bearing inputs change and stale judgment is reused | complete governing-basis identity invalidates reuse on any change |
| INT-003 | R28, R29, R31, R32, R33, R35 | BND-INPUT-001, BND-STATE-001, BND-AUTH-001 | one non-approval status over-mutates unaffected targets or creates partial approval | evidence-scoped dispositions mutate only supported targets and approve none |
| INT-004 | R37, R38, R39, R41, R42, R43, R44, R45 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | interruption forces retry to reconstruct intended writes from mutable current state | complete prepared evidence precedes writes and exact retry completes only recorded pending work |
| INT-005 | R8, R9, R10, R50, R51, R54, R55, R57 | BND-COMPOSE-001, BND-COMPAT-001 | progressive disclosure changes shared bytes, hides semantic loss, or drifts packaged resources | byte parity, owner ledgers, real-profile measurement, and package parity remain mandatory |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | regression | R20, R23, R24 | BND-AUTH-001 | ARRSIM-R2-PR1 | - |
| E2 | illustration | R3, R6 | BND-COMPOSE-001 | - | - |
| E3 | illustration | R7 | BND-COMPOSE-001, BND-RECOVERY-001 | - | - |
| E4 | regression | R21, R26, R27 | BND-AUTH-001 | ARRSIM-R2-PR1 | - |
| E5 | regression | R28, R31, R35 | BND-STATE-001 | ARRSIM-R2-PR2 | - |
| E6 | regression | R28, R33 | BND-STATE-001 | ARRSIM-R2-PR2 | - |
| E7 | regression | R37, R38 | BND-STATE-001, BND-RECOVERY-001 | ARRSIM-R2-PR3 | - |
| E8 | regression | R42, R43, R44 | BND-TEMPORAL-001, BND-RECOVERY-001 | ARRSIM-R2-PR3 | - |
| E9 | illustration | R41, R45 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E10 | illustration | R17, R18 | BND-AUTH-001, BND-ENV-001 | - | - |
| E11 | regression | R8, R9, R10 | BND-COMPOSE-001, BND-COMPAT-001 | ARRSIM-PR1 | - |
| E12 | regression | R12, R13, R14 | BND-INPUT-001 | ARRSIM-PR2 | - |

## Compatibility and migration

The migration is prospective for the canonical `architecture-review` package. Existing historical review records remain readable and unchanged. The main skill, two references, directly coupled validators and fixtures, resource inventories, and generated package metadata migrate atomically. The shared isolation and recording block remains byte-identical. Rollback restores the previous flat skill, removes both references, restores coupled expectations, and regenerates derived packages without rewriting historical reviews.

## Observability

The change is observable through resource maps, semantic and literal ledgers, static scenario results, profile and package measurements, shared-block byte comparison, lifecycle validation, review evidence, target dispositions, prepared-manifest progress, and canonical-through-installed package parity. Reports distinguish configured commands from executed commands and relocated procedure from removed behavior.

## Security and privacy

The change introduces no credentials, network operation, external persistence, or personal-data processing. Unsafe paths, escaped resources, unrecorded targets, stale authority, and unrelated files fail closed. Existing destructive-action, publication, and external-state boundaries remain mandatory.

## Accessibility and UX

Not applicable to end-user interface accessibility. Published Markdown must remain readable, keep complete prose sentences intact, retain stable IDs and tables, and emit no placeholders.

## Performance expectations

`ARR1-recorded` and `ARR1M-recorded-method` must use fewer LF-normalized UTF-8 bytes and Unicode whitespace-separated words than their baselines. Every assembly, reference, and total package size is reported separately, and no runtime latency contract is introduced.

## Edge cases

EC1. A formal record-only review has no stable subject identity: recording blocks and no lifecycle target is invented.

EC2. An architecture method contract changes after review: identical retry is rejected and a new occurrence is required.

EC3. One material finding names one ADR in a combined subject: only that ADR becomes `revision-required`; all other targets remain unsettled.

EC4. A review-occurrence blocker prevents durable recording: no target settlement occurs.

EC5. A target-set-wide conflict is evidenced: every exact target may become `blocked` without implying partial approval.

EC6. A manifest is prepared but no target changed: exact retry revalidates and begins pending writes.

EC7. One target already matches its expected post-state and manifest progress: retry verifies it and does not duplicate settlement evidence.

EC8. A target state changed independently after preparation: retry blocks without adoption.

## Non-goals

- Redesigning the C4, arc42, ADR, canonical-package, or four-surface architecture-review method.
- Adding an output asset, runtime router, semantic classifier, transcript grader, tokenizer, target-agent journey, or separate manual semantic gate.
- Creating a rationale lifecycle artifact, new review status, partial semantic approval, lifecycle state, or workflow-routing owner.
- Optimizing `architecture`, another review skill, or the generic formal-review evidence model beyond directly required compatibility.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every R-clause maps to deterministic proof in the test specification. |
| AC2 | The package contains one universal skill and exactly two mapped conditional references with no new asset. |
| AC3 | The shared isolation and recording subsection remains byte-identical inline. |
| AC4 | All four surfaces, four loaded assemblies, six valid authority combinations, and representative invalid combinations have direct proof. |
| AC5 | Every formal review binds an exact subject and governing basis independently from optional settlement targets. |
| AC6 | Non-approved review approves no target and mutates only targets supported by finding-scoped or blocker-scoped evidence. |
| AC7 | Prepared settlement evidence exists before every target mutation scenario and exact partial retry adopts no changed state. |
| AC8 | Semantic and literal ledgers give every current rule and compatibility dependency one disposition. |
| AC9 | Primary formal loaded profiles decrease while total package growth remains visible and justified. |
| AC10 | Canonical-through-installed resource inventories and raw bytes match. |
| AC11 | Acceptance executes no target-agent runtime and introduces no separate manual semantic-review gate. |
| AC12 | Architecture assessment returns `architecture-required` if existing formal-review evidence cannot safely carry the prepared manifest. |

## Open questions

None. Exact manifest field names and fixture serialization may vary while preserving R37 through R45 and must be settled by architecture assessment, planning, and the test specification.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Execution plan and test specification after required review settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This artifact does not claim review approval, architecture settlement, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.
