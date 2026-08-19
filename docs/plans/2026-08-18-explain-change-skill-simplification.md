# Explain-Change Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `explain-change` package without weakening actual-diff grounding, governed closeout, refresh safety, reviewed-subject identity, or workflow and verification claim boundaries. Freeze semantic and literal ownership first, split the canonical package second, and prove all-profile reduction and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-18-explain-change-skill-simplification.md`
- Spec: `specs/explain-change-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260818-ordered-final-review-stage-evidence-tail.md`
- Architecture review: `docs/changes/2026-08-18-explain-change-skill-simplification/reviews/architecture-review-r1.md`
- Test spec: `specs/explain-change-skill-simplification.test.md`, pending revision for the ordered evidence tail

## Context and orientation

`skills/explain-change/` is the only authored package source. The current flat `SKILL.md` mixes universal explanation quality, governed final-review and review-resolution procedure, and durable Markdown structure. The change adds `references/governed-workflow-explanation.md` and `assets/explain-change-skeleton.md`, keeps four real assemblies, and changes no workflow order or stage owner.

The package simplification and its first three implementation milestones are complete, but final review found that one explanation-only direct-child commit cannot also preserve durable final-review evidence. The approved amendment and ADR replace that incomplete model with exact non-merge direct-child revisions `S -> R -> E`: reviewed subject, final-review recording, and explanation plus workflow handback. Existing build and adapter tooling continues to own generated-resource parity.

## Non-goals

- Change final review, review-resolution, workflow, verify, PR, or lifecycle-state ownership; the new revisions compose existing owners only.
- Add section-level refresh, managed Markdown regions, historical-layout parsing, partial-write transactions, a new identity service, or change-record writes by `explain-change`.
- Add scripts, executable generation, model-runtime grading, tokenizer dependencies, or target-agent acceptance.
- Bulk-migrate historical explanations or optimize another skill beyond directly coupled compatibility surfaces.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R36-R44; BND-COMPAT-001, BND-ENV-001; INT-005 | M1 rule/literal ledgers, architecture-trigger check, deterministic scenarios, and baselines |
| R1-R23, R30-R35; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001; INT-001, INT-002, INT-004 | M2 focused contract alignment, canonical package split, whole-file refresh, and handback |
| R36-R43; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005 | M3 semantic preservation, four-profile reduction, boundary proof, and canonical-through-installed parity |
| R24-R29; BND-TEMPORAL-001, BND-RECOVERY-001; INT-003 | M4 four-part code-state identity, exact `S -> R -> E` ownership validation, retry, and end-to-end Git proof |
| R1-R44 | M5 final review, ordered evidence commits, explanation, and verify closeout |

## Milestones

### M1. Freeze rules, literals, scenarios, and profile baselines

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule, consumed literal, boundary scenario, and real loaded assembly before canonical procedure moves.
- Requirements: R36-R44; BND-COMPAT-001; BND-ENV-001; INT-005.
- Architecture decisions: none for the preservation inventory; its identity inventory later exposed the gap now resolved by ADR-20260818 and M4.
- Files/components likely touched:
  - `docs/changes/2026-08-18-explain-change-skill-simplification/explain-change-rule-disposition.yaml`
  - `docs/changes/2026-08-18-explain-change-skill-simplification/explain-change-literal-compatibility.yaml`
  - `docs/changes/2026-08-18-explain-change-skill-simplification/fixtures/`
  - `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved specification, clean spec review, and recorded architecture assessment
  - current skill, workflow and skill contracts, parser consumers, validators, package mappings, and generated-resource owners
- Tests and proof:
  - closed rule and literal vocabularies reject unknown values before consistency checks
  - every universal, governed, structural, parser-sensitive, incidental, retained, relocated, amended, or removed item has one disposition
  - scenarios cover all signal classes, actions, assemblies, target states, refresh authorities, atomic outcomes, reviewed-subject tails, handback claims, historical artifacts, and missing resources
  - LF-normalized 1,175-word and 8,224-byte baseline is independently reproduced
  - the identity and recovery inventory confirms that no R44 architecture trigger is required before M2
- Implementation steps:
  - inventory current skill rules and all exact consumers of final-diff, final-review, review-resolution, readiness, path, result, and package literals
  - classify rule and literal ownership without freezing incidental prose
  - serialize deterministic positive and negative scenarios with unknown-value cases
  - record canonical input identities and the EC0-EC3 measurement formula
  - stop and return to architecture if existing evidence cannot represent the approved reviewed-subject and closed-tail contract
- Validation commands:
  - `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, scenario, consumer, and measurement input has one closed treatment before canonical package mutation.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, baselines are reproducible, no R44 trigger is present, and `skills/explain-change/SKILL.md` remains unchanged.
- Required evidence: `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence.
- Optional commit boundary: `M1: freeze explain-change simplification ownership`
- Risks:
  - parser-sensitive literals may be mistaken for semantic owners
  - a hidden workflow consumer may depend on misleading readiness wording
- Rollback/recovery:
  - revert M1 evidence only; return normative gaps to spec and architecture triggers to architecture assessment before M2

### M2. Align the contract and split the canonical package

- Milestone kind: implementation
- Goal: Shorten the universal skill, add the governed reference and skeleton, and implement closed action, refresh, and handback behavior. M4 supersedes the incomplete evidence-tail portion discovered at final review.
- Requirements: R1-R23, R30-R35; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; INT-001; INT-002; INT-004.
- Architecture decisions: existing published-skill resource and stage-owned evidence architecture; no ADR.
- Files/components likely touched:
  - `skills/explain-change/SKILL.md`
  - `skills/explain-change/references/governed-workflow-explanation.md`
  - `skills/explain-change/assets/explain-change-skeleton.md`
  - `scripts/workflow_automation_state.py`
  - `scripts/workflow_automation.py`
  - `scripts/test-workflow-automation-state.py`
  - `scripts/test-workflow-automation.py`
  - `scripts/test-skill-validator.py`
  - directly coupled specification or workflow wording identified by M1
- Dependencies:
  - M1 and its code review close with no architecture reassessment trigger
- Tests and proof:
  - tri-state governed signals, three actions, four assemblies, late loading, and missing-resource stops
  - create/refresh state and authority matrices, current-skeleton composition, atomic replacement, concurrency, uncertain read-back, and fresh retry
  - governed closeout, concise review-resolution summary, explanation metadata, and neutral `Workflow handback`
  - forbidden lifecycle, readiness, external, and cross-stage mutations
- Implementation steps:
  - add failing focused assertions and scenario fixtures before canonical edits
  - keep universal truthfulness, diff, privacy, stops, claims, and resource selection inline
  - move only governed eligibility, placement, final-review and review-closeout interpretation, basis, staleness, and handback procedure into the reference
  - copy complete durable structure into the skeleton and use it for every create and refresh
  - update only directly coupled active consumers identified by M1
- Validation commands:
  - `python scripts/validate-skills.py skills/explain-change/SKILL.md`
  - `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: each invocation loads its exact assembly, durable output is safely replaced, reviewed code remains distinct from explanation evidence, and handback makes no readiness claim.
- Completion criteria: focused and broad tests pass, every rule and structure has one owner, existing literals remain compatible or migrate atomically, and no new architecture owner appears.
- Required evidence: `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the focused contract, canonical package, and coupled consumers.
- Optional commit boundary: `M2: simplify explain-change package paths`
- Risks:
  - universal evidence safety may move behind governed loading
  - Git-tail logic may accept unrelated changes or reject the explanation's own commit
  - skeleton fields may become hidden policy
- Rollback/recovery:
  - restore the prior canonical skill and coupled consumers atomically, remove mapped resources, and rebuild generated packages

### M3. Prove four-profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove semantic preservation, all-profile reduction, boundary coverage, and canonical-through-installed integrity.
- Requirements: R36-R43; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-005.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct resource-selection proof is absent
  - `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - EC0-EC3 each decrease in words and UTF-8 bytes from baseline; resource and total package sizes remain visible
  - every semantic rule and consumed literal has one verified final disposition
  - generated, archived, release-candidate, and clean-installed packages contain exact required resources and reject drift
  - every applicable boundary and selected interaction has direct proof
- Implementation steps:
  - extend only existing package proof if direct explain-change selection coverage is absent
  - build and validate temporary package and installation trees
  - report before/after assemblies, individual resources, duplicate ownership, and total package
  - compare the final package and coupled consumers with the M1 ledgers and approved requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/explain-change/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/explain-change-skill-simplification.md`
  - `python scripts/build-skills.py --check`
- Expected observable result: all four assemblies shrink and every supported package carries byte-identical required resources and semantics.
- Completion criteria: measurement, preservation, boundary, canonical, generated, archive, release-candidate, and clean-install proof pass with no unexplained growth or unresolved literal.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M3: prove explain-change simplification`
- Risks:
  - generic adapter tests may omit one assembly or asset mapping
  - a smaller root may hide governed-profile growth
- Rollback/recovery:
  - restore the prior package, regenerate derived output, and discard temporary trees

### M4. Implement and prove the ordered final-review evidence tail

- Milestone kind: implementation
- Goal: Replace the impossible one-commit final-review reuse rule with the approved four-part identity model and exact `S -> R -> E` validation.
- Requirements: R24-R29; BND-TEMPORAL-001; BND-RECOVERY-001; INT-003.
- Architecture decisions: ADR-20260818 ordered final-review stage-evidence tail.
- Files/components likely touched:
  - `scripts/workflow_code_state.py`
  - `scripts/workflow_automation.py`
  - `scripts/test-workflow-code-state.py`
  - `scripts/test-workflow-automation.py`
  - `scripts/test-skill-validator.py`
  - `skills/explain-change/SKILL.md`
  - `skills/explain-change/references/governed-workflow-explanation.md`
  - directly coupled fixture, rule-ledger, literal-ledger, workflow, and verification wording
- Dependencies:
  - approved spec revision and accepted ADR-20260818
  - approved architecture-review-r1
  - revised test specification and approving test-spec review
- Tests and proof:
  - code-state resolution exposes reviewed subject `S`, final-review recording `R`, explanation recording `E`, and handoff revision `E` without self-referential tracked hashes
  - exact non-merge direct-child ancestry and the allowed `S -> R` retry state pass
  - reordered, merged, intervening, unrelated-path, unknown-field, changed-basis, and recorded/Git identity mismatch cases fail closed
  - semantic diff validation admits only the closed final-review fields in `R` and handback fields in `E` for shared `change.yaml`
  - one real temporary Git repository proves `S -> R -> E -> verify` and the later verify-owned evidence boundary
- Implementation steps:
  - add failing focused unit and temporary-repository tests before implementation changes
  - extend the code-state anchor and workflow integration to the four revision roles
  - add path-and-field manifests for `R` and `E`, including safe YAML semantic comparison for `change.yaml`
  - replace the obsolete one-direct-child wording in the published explain-change package and coupled fixtures while preserving existing result labels
  - update the preservation ledgers and evidence only for the amended contract
  - run focused validation before broad workflow and package checks
- Validation commands:
  - `python scripts/test-workflow-code-state.py`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests`
  - `python scripts/validate-skills.py skills/explain-change/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: workflow and verify distinguish `S`, `R`, and `E`, reuse final review only for the exact closed tail, and recover only from exact `S -> R` without accepting unrelated lifecycle edits.
- Completion criteria: focused and broad tests pass, the real Git scenario proves the complete sequence, every negative tail and field case fails closed, published guidance matches the approved model, and no new persistence or write owner appears.
- Required evidence: `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/m4-ordered-evidence-tail.md`
- Review handoff: independent `code-review` of M4 code-state, semantic-diff, workflow-integration, published-guidance, and end-to-end proof changes.
- Optional commit boundary: `M4: implement ordered final-review evidence tail`
- Risks:
  - YAML field comparison may accidentally admit unrelated nested changes
  - tests may prove synthetic hashes without exercising real Git ancestry
  - old one-commit wording may survive in a fixture or generated consumer
- Rollback/recovery:
  - revert M4 as one unit to the blocked pre-closeout state; do not restore the obsolete one-commit readiness claim or proceed to verify

### M5. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R44.
- Architecture decisions: ADR-20260818.
- Files/components likely touched:
  - final review records, `explain-change.md`, and `verify-report.md` under the owning change root
- Dependencies:
  - M1-M4 and required review resolution are closed
- Tests and proof:
  - final holistic diff review and the complete approved test-spec command ledger
- Implementation steps:
  - commit the final reviewed subject as `S`
  - run final holistic `code-review` and record its exact evidence and settlement in direct-child `R`
  - create or refresh the explanation and record workflow handback in direct-child `E`
  - run final `verify` against the exact ordered tail and record later verify-owned evidence separately
- Validation commands:
  - use the complete approved test-spec commands
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: implementation evidence is coherent and final verification reports truthful PR handoff state.
- Completion criteria: final review is clean, rationale is current, verification is recorded, and no blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate authority.
- Optional commit boundary: `closeout: verify explain-change simplification`
- Risks:
  - late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 focused skill-validator proof owns closed ledgers, static scenarios, unknown-value-first behavior, architecture triggers, and baselines.
- M2 focused and broad skill/workflow validation owns classification, resource selection, whole-file refresh, evidence tails, handback, and forbidden writes.
- M3 adapter, build, boundary, and measurement proof owns generated-resource parity and semantic preservation.
- M4 focused code-state, workflow, skill, semantic-diff, and real-Git proof owns the ordered evidence-tail behavior.
- Change metadata, formal reviews, code review, verify, and PR review own lifecycle and human judgment.

## Risks and recovery

- Risk: extraction hides universal truthfulness. Recovery: block M2 on M1 ownership and EC0 proof.
- Risk: evidence-tail composition weakens final review. Recovery: accept only exact `S -> R -> E`, validate shared state by field, and negative-test every broader or reordered tail.
- Risk: relocation appears as deletion. Recovery: report all assemblies, individual resources, duplicate ownership, and total package.
- Risk: a new identity owner is needed. Recovery: stop and return to architecture before canonical mutation.

## Dependencies

- Approved spec revision, clean spec review, accepted canonical architecture and ADR-20260818, and the accepted portable proposal direction.
- Existing published-skill resource, stage-owned lifecycle, workflow automation, final-review, verify, and adapter-package contracts.
- Existing skill validation, package generation, archive validation, release-candidate validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-18 | Use three implementation milestones plus lifecycle closeout. | Inventory, package mutation, and distribution proof have distinct rollback and review boundaries. | One large rewrite; prose-only milestones. |
| 2026-08-18 | Preserve existing evidence labels while clarifying their identity semantics. | This avoids a new persistence owner and maintains active consumers. | New transaction schema; self-referential commit metadata. |
| 2026-08-18 | Make every durable refresh a current-skeleton whole-file replacement. | One structural rule closes loading, authority, and recovery without a Markdown ownership parser. | Section updates; historical-layout preservation. |
| 2026-08-18 | Measure every assembly and total package separately. | Root-only reduction cannot prove user value. | EC0-only or workflow-only measurement. |
| 2026-08-18 | Add one implementation milestone for exact `S -> R -> E` evidence-tail support before lifecycle closeout. | The approved amendment changes code-state identity, semantic diff validation, recovery, published guidance, and end-to-end proof; hiding it in closeout would make it unreviewable. | Patch during verify; fold behavior into lifecycle closeout; reopen completed M1-M3. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
