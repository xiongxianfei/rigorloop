<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->

# Code-Review Skill Simplification

## Owning change record

`docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-10-code-review-skill-simplification.md`

## Goal and context

This specification defines the behavior-preserving simplification contract for the published `code-review` skill package.
It narrows the common-path `SKILL.md`, gives repeated rules one owner, moves workflow-managed automation procedure behind one mapped conditional reference, and uses existing assets as the only copy-and-fill output structures.

The change preserves review status, finding, recording, proof, milestone, and handoff semantics.
It does not certify target-agent behavior, grade model output, or make a numeric reduction target authoritative over semantic preservation.

This specification specializes `specs/skill-contract.md` for `code-review` and operates within the deterministic acceptance boundary established by `specs/published-skill-first-repository-simplification.md`.
Where an earlier clause could be read as limiting the governing skill to the literal `SKILL.md` body, this specification defines the governing published `code-review` skill as the complete canonical package described in R1.

## Glossary

- **governing skill package**: canonical `skills/code-review/SKILL.md` plus every explicitly mapped packaged reference and structural asset beneath `skills/code-review/`.
- **common path**: instructions loaded from `SKILL.md` for every direct, isolated, formal, or workflow-managed invocation before any conditional reference is read.
- **conditional automation reference**: `references/workflow-managed-automated-review.md`, loaded only for a formally armed workflow-managed automated review or correction loop.
- **universal policy**: review behavior that applies before or independently of conditional-reference loading.
- **rule-disposition ledger**: the change-local source-to-destination accounting for every behaviorally significant current rule or repeated rule cluster.
- **material common-path reduction**: a smaller `SKILL.md` with every identified duplication cluster consolidated and no behaviorally significant rule lost; it is not defined by a fixed percentage.
- **fixture-based contract proof**: deterministic scenario data that states required and forbidden outcomes without executing or grading an agent runtime.
- **structural asset**: a mapped copy-and-fill artifact template that owns repeated output structure but no review policy.

## Examples first

### Example E1: direct review does not load automation procedure

Given a direct or isolated `code-review` invocation
When the reviewer follows the common path
Then `SKILL.md` supplies review authority, evidence, checklist, statuses, recording, stops, claims, and handoff without loading `workflow-managed-automated-review.md`.

### Example E2: workflow-managed automation loads one conditional reference

Given a formally armed workflow-managed automated review or correction loop
When the common path reaches the automation load trigger
Then the reviewer reads `references/workflow-managed-automated-review.md` and applies its automation-only phases without transferring ownership away from `code-review`.

### Example E3: missing conditional reference fails package integrity

Given `SKILL.md` maps `references/workflow-managed-automated-review.md`
When the canonical, generated, packed, or installed package lacks that resource or contains stale untransformed bytes
Then deterministic package validation fails with the affected target, missing or stale path, and repair action.

### Example E4: an unknown ledger disposition fails closed

Given a rule-disposition entry uses `moved-somewhere`
When the ledger is reviewed or structurally checked
Then the entry is invalid because the value is outside the closed disposition vocabulary.

### Example E5: safe reduction below the planning target may pass

Given common-path tokens decrease by less than 35 percent
When the ledger accounts for every rule, all duplication clusters have one owner, direct review is materially shorter, and semantic review finds further compression would hide universal policy
Then the change may satisfy this specification with the measured shortfall and rationale recorded.

### Example E6: runtime execution is rejected as acceptance proof

Given a proposed check would start Codex, Claude Code, opencode, or another model and grade its response
When acceptance evidence is selected
Then that check is rejected and proof remains deterministic fixtures plus independent semantic review.

### Example E7: output structure is asset-owned

Given a review result or material finding is produced
When its repeated field structure is needed
Then the mapped asset owns the structure and `SKILL.md` does not carry a second full copy.

## Requirements

R1. The governing published `code-review` skill MUST consist of canonical `skills/code-review/SKILL.md` plus every explicitly mapped packaged reference and structural asset under the same skill root, while lifecycle, review, policy, and readiness ownership remains solely with `code-review`.

R2. `SKILL.md` MUST remain sufficient for every direct or isolated review without loading the conditional automation reference.

R3. `SKILL.md` MUST keep purpose and trigger, workflow role and ownership, review-surface and governing-authority resolution, the core checklist, review statuses, severity, material-finding fields, isolation and recording, direct-proof obligations, universal stop conditions, claim boundaries, status-to-handoff behavior, milestone-local versus final-review behavior, the compact boundary-first bridge, and every resource load trigger inline.

R4. `SKILL.md` MUST map exactly one automation-policy reference at `references/workflow-managed-automated-review.md` with the literal verb `READ` and an exact load condition limited to a formally armed workflow-managed automated review or correction loop.

R5. The conditional automation reference MUST own only automated independent-review phases, automation packet handling, requirement-fidelity procedure, automation-only risk and review checks, reviewer-owned auto-fix classification, bounded correction and rereview procedure, phase receipts, promotion, and automation-specific pause or failure handling.

R6. The conditional automation reference MUST NOT own material-finding meaning, native review-status semantics, downstream-blocking rules, claim boundaries, formal review recording, universal stop conditions, or the requirement to rereview changed code.

R7. The mapped review-result and material-finding assets MUST be the sole copy-and-fill owners for repeated output structure; assets MUST NOT own review policy.

R8. The implementation change MUST create `docs/changes/2026-08-10-code-review-skill-simplification/code-review-rule-disposition.yaml` and assign every behaviorally significant current rule or repeated rule cluster one stable rule ID, source locations, behavior summary, governing requirement IDs, destination, and disposition.

R9. Rule disposition MUST use exactly one of `retained-inline`, `retained-conditional-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; unknown or missing values MUST fail closed before consistency checks.

R10. No behaviorally significant rule MAY disappear; `removed-obsolete-with-approved-contract-change` MUST cite the approving contract change, and every other disposition MUST resolve to an in-scope destination or documented duplicate owner.

R11. The implementation MUST consolidate these identified duplication clusters to one owner: quick-guide restatement, evidence-reading guidance, claim boundaries, handoff and milestone routing, full inline output templates, shared boundary-method detail, and workflow-managed automation procedure.

R12. Acceptance MUST require material common-path reduction, complete ledger coverage, one owner for every repeated rule, no semantic or lifecycle loss, and separate common-path and total-package accounting.

R13. A 35–45 percent common-path word or token decrease MUST remain a non-normative planning target; falling below it MUST NOT fail acceptance when semantic review and the ledger show that further reduction would hide universal policy or reduce clarity, while no material common-path reduction MUST fail the proposal objective.

R14. Change evidence MUST report before-and-after `SKILL.md` lines, words, and tokenizer count; conditional-reference words and tokens; total package words and tokens; duplicated rule-cluster count; inline-template count; and mapped-resource count.

R15. Acceptance proof MUST use exactly three classes: deterministic structural proof, fixture-based contract proof, and independent semantic review of the complete skill package and rule-disposition ledger.

R16. Fixture-based contract proof MUST cover direct review, formal recorded review, missing governing authority, material finding, clean non-final milestone, clean final milestone, and workflow-managed automated review, with explicit required and forbidden outcomes and without executing a model.

R17. Independent semantic review MUST assess trigger clarity, package ownership, prerequisites, operating sequence, evidence use, stop conditions, claim boundaries, output usefulness, handoff clarity, rule dispositions, and the exact conditional-reference load trigger.

R18. Implementation, verification, release, and repository acceptance MUST NOT start Codex, Claude Code, opencode, or another target-agent runtime; send prompts; grade transcripts; maintain model-selection or runtime-version evidence; retry nondeterministic runs; or claim deterministic model routing.

R19. Permanent deterministic validation MUST remain limited to existing owners for frontmatter and required structure, closed vocabularies, Resource map syntax, mapped-resource existence and containment, placeholder absence, narrow forbidden claims, generated package inventory, and canonical-to-generated or packed resource parity.

R20. This change MUST NOT add a standalone simplification validator, permanent line or token budget gate, prose-quality score, selector, scheduler, validation cache, or model-runtime journey test.

R21. Canonical, generated, packed, and installed supported package targets MUST include every mapped reference and asset at its declared relative path with required raw-byte parity for untransformed resources.

R22. A missing, path-escaping, unfilled, stale, or undeclared mapped resource MUST fail deterministic package validation before publication and MUST identify the affected target, invariant, and repair surface.

R23. Review status vocabulary, severity, material-finding requirements, formal recording, review settlement, milestone behavior, downstream authority, and historical review-artifact validity MUST remain unchanged.

R24. The change MUST receive a recorded architecture assessment after approving spec review; the assessment MUST choose `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`, and ambiguity MUST pause workflow automation.

R25. Rollout MUST update canonical `SKILL.md`, mapped resources, and generated package proof atomically; rollback MUST restore the prior complete canonical package and regenerate derived packages without leaving a partial reference move.

## Boundary model

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R2, R4, R8, R9, R15, R16 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R4, R5, R6, R16, R23, R24, R25 | BND-STATE-001 | - |
| identity-authority | applicable | R1, R3, R5, R6, R7, R10, R17, R19 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R4, R7, R11, R21, R22 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R4, R5, R16, R23, R25 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R9, R10, R13, R18, R22, R24, R25 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R19, R21, R23, R25 | BND-COMPAT-001 | - |
| external-environment | applicable | R15, R16, R18, R21, R22 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R2, R4, R8, R9, R15, R16 | direct, isolated, formal, workflow-managed automated; valid, missing, unknown ledger value | Invocation mode selects only applicable procedure; every ledger value is closed and every scenario uses an approved proof class. | Direct modes continue inline; armed automation loads the reference; missing or unknown inputs fail or stop. | R4 |
| BND-STATE-001 | state-lifecycle | R4, R5, R6, R16, R23, R24, R25 | common path -> conditional load -> automated phases -> native verdict -> handoff; spec review -> architecture assessment | Conditional procedure never changes native status, settlement, milestone, or workflow authority. | Valid stages advance through existing outcomes; ambiguous architecture or invalid transition pauses. | R23 |
| BND-AUTH-001 | identity-authority | R1, R3, R5, R6, R7, R10, R17, R19 | `code-review` package, inline policy, conditional procedure, structural assets, semantic review, deterministic validation | `code-review` owns behavior; references own only mapped detail; assets own structure; validators own only deterministic facts. | Correct owner decides; misplaced policy or semantic validator claims fail review. | R1 |
| BND-COMPOSE-001 | composition-path | R1, R2, R4, R7, R11, R21, R22 | canonical `SKILL.md` + boundary reference + automation reference + assets -> generated and packed targets | Every declared resource exists, is mapped once, stays under the skill root, and preserves required parity. | Complete packages pass; missing, stale, escaped, or duplicate ownership fails. | R21 |
| BND-TEMPORAL-001 | temporal-retry | R4, R5, R16, R23, R25 | initial review, correction, rereview, final holistic review; old package -> atomic new package -> rollback | Rereview and correction retain the original target and native verdict semantics; package versions never mix. | Corrected work is rereviewed; partial or stale rollout stops; rollback restores one complete prior package. | R25 |
| BND-RECOVERY-001 | failure-recovery | R9, R10, R13, R18, R22, R24, R25 | invalid ledger, unsafe compression, runtime-proof request, missing resource, ambiguous architecture, partial rollout | Unknown or unsafe states fail closed and preserve the last valid contract or package. | Repair routes to ledger, spec, package, or architecture owner; runtime proof is rejected; rollback remains available. | R22 |
| BND-COMPAT-001 | compatibility-migration | R19, R21, R23, R25 | historical review records, current package, generated targets, rollback package | Existing review semantics and historical evidence remain valid while supported package targets receive equivalent content. | Current artifacts remain readable; new packages adopt atomically; rollback does not rewrite history. | R23 |
| BND-ENV-001 | external-environment | R15, R16, R18, R21, R22 | repository files, deterministic fixtures, local generated or packed trees, target-agent runtime, network | Acceptance uses repository-owned deterministic artifacts and semantic review, never target-runtime execution or network model calls. | Local deterministic proof may pass or fail; model execution is rejected as acceptance evidence. | R18 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R2, R3, R4 | BND-INPUT-001, BND-COMPOSE-001 | A direct review needs universal policy that was moved to the automation reference. | Direct and isolated review remains complete from `SKILL.md`; the ledger rejects misplaced universal policy. |
| INT-002 | R1, R5, R6, R7 | BND-AUTH-001, BND-COMPOSE-001 | A reference or asset becomes a separate policy owner. | Ownership remains at `code-review`; references own conditional detail and assets own structure only. |
| INT-003 | R21, R22, R25 | BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001 | Canonical `SKILL.md` points to a resource absent or stale in one generated target. | Package validation blocks publication and rollback restores a complete package. |
| INT-004 | R12, R13, R14, R17 | BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001 | A numeric target causes universal policy deletion or disguised relocation. | Ledger and semantic review override the target; common-path and total-package metrics remain separate. |
| INT-005 | R15, R16, R18, R20 | BND-AUTH-001, BND-ENV-001 | A fixture scenario expands into live model execution or transcript grading. | Acceptance stops at deterministic fixtures and independent semantic review. |
| INT-006 | R4, R5, R23, R25 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | A partial automation-policy move changes rereview or native verdict behavior. | Atomic rollout or rollback preserves one complete policy version and unchanged native review semantics. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R2, R4 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E2 | illustration | R4, R5 | BND-STATE-001 | - | - |
| E3 | illustration | R21, R22 | BND-COMPOSE-001 | - | - |
| E4 | illustration | R9 | BND-INPUT-001, BND-RECOVERY-001 | - | - |
| E5 | illustration | R13 | BND-RECOVERY-001 | - | - |
| E6 | illustration | R15, R16, R18 | BND-ENV-001 | - | - |
| E7 | illustration | R7 | BND-AUTH-001, BND-COMPOSE-001 | - | - |

## Inputs and outputs

Inputs:

- the accepted proposal and approved proposal-review evidence;
- the current canonical `code-review` package;
- governing skill, package-integrity, workflow-automation, requirement-fidelity, review-recording, and published-skill-first contracts;
- current generated and packed adapter target declarations;
- existing deterministic validation owners.

Outputs:

- a simplified canonical `SKILL.md`;
- one mapped workflow-managed automation reference;
- retained mapped boundary reference and structural assets;
- a complete change-local rule-disposition ledger;
- deterministic scenario fixtures and selected validation evidence;
- before-and-after common-path and package measurements;
- independent semantic review evidence.

## State and invariants

- `skills/code-review/` remains the only authored package source.
- `code-review` remains the only stage, lifecycle, review, and readiness owner for its package.
- Universal policy remains inline before any conditional load.
- Conditional procedure cannot redefine native verdicts or workflow routing.
- Assets own structure only.
- Every current rule is accounted for exactly once in the ledger.
- Unknown closed-vocabulary values fail before consistency logic.
- Common-path reduction never substitutes for semantic preservation.
- Generated package trees remain derived and equivalent for supported targets.

## Error and boundary behavior

- A missing or ambiguous invocation mode uses the universal inline contract and does not load automation procedure unless the formal armed trigger is proved.
- A missing, duplicated, escaped, stale, or undeclared mapped resource fails deterministic package proof.
- An unknown or missing ledger disposition fails closed and blocks implementation closeout.
- A rule without a destination or approved obsolete-contract citation blocks semantic preservation.
- A proposed runtime journey, transcript grade, model selector, or nondeterministic retry is rejected as out of scope.
- A percentage shortfall requires recorded semantic rationale; it does not fail by itself.
- No material common-path reduction fails acceptance even when all deterministic structure checks pass.
- Architecture ambiguity pauses the workflow before planning.
- A partial package move rolls back to the last complete package.

## Compatibility and migration

Existing review records, status values, severities, finding fields, milestone states, and handoff meanings remain valid.
No artifact migration is required.

The package change is atomic across canonical source and supported generated package proof.
Historical package archives remain historical evidence and are not rewritten.
Rollback reverts the canonical package revision and regenerates derived packages from that revision.

This specification does not relax existing deterministic skill, resource, archive, or adapter parity requirements.
It narrows acceptance by explicitly excluding target-agent runtime proof consistently with the published-skill-first contract.

## Observability

Change-local evidence records:

- the rule-disposition ledger identity and coverage count;
- before-and-after common-path and total-package measurements;
- identified duplication clusters and final owners;
- deterministic fixture results;
- selected existing validation commands and outcomes;
- semantic review result and any residual limits;
- generated target and resource parity results.

Diagnostics identify the affected artifact or target, violated invariant, and repair surface.
No model ID, prompt, transcript, runtime retry, or external publication status is recorded as acceptance proof.

## Security and privacy

Acceptance uses repository-local source, fixtures, temporary generated package trees, and review artifacts.
It MUST NOT require credentials, private prompts, model transcripts, network model access, user data, or machine-local paths.
Mapped-resource validation rejects path traversal outside the skill root.

## Accessibility and UX

No graphical user interface is introduced.
The simplified common path and diagnostics use clear headings, stable identifiers, and actionable plain-language repair guidance.

## Performance expectations

Common-path lines, words, and tokenizer count MUST decrease materially from the recorded baseline.
The 35–45 percent range is a planning target only.
Total-package growth is allowed only when the conditional reference explains the delta and semantic review confirms that common-path loading and ownership improved.

No runtime or maintenance-cost target may override rule preservation, deterministic parity, or review quality.

## Edge cases

EC1. A rule applies to direct and automated review: retain the universal portion inline and place only automation-specific procedure in the conditional reference.

EC2. Two repeated paragraphs differ slightly: the ledger records one semantic owner and preserves any distinct behavior before removing the duplicate wording.

EC3. An existing inline output example carries policy as well as structure: keep policy inline and move only repeated fields to the asset.

EC4. A generated target transforms the new reference intentionally: require an existing approved transformation contract rather than treating unequal bytes as ordinary parity.

EC5. A direct review mentions workflow automation for context: do not load the conditional reference unless the invocation is formally armed.

EC6. The new reference is present but not mapped: package validation fails because unreferenced packaged policy is not discoverable through the skill contract.

EC7. A rule appears obsolete but no approved contract change exists: use a retained disposition or route the contract change upstream; do not remove it.

EC8. The measured common path drops sharply because policy moved to multiple references: fail semantic review because R4 permits exactly one automation-policy reference and universal policy must remain inline.

EC9. Architecture assessment finds existing resource-integrity architecture sufficient: record `architecture-required` when architecture documentation still needs a package-boundary update, or `architecture-not-required` only when no architecture artifact changes are necessary.

## Non-goals

- Simplifying another skill.
- Changing native review outcomes, finding semantics, lifecycle state, milestone routing, or workflow stage order.
- Creating a new skill, stage, runtime service, persistent store, API, or user interface.
- Certifying target-agent interpretation or deterministic routing.
- Adding prompt journeys, transcript grading, model matrices, runtime-version evidence, or nondeterministic retries.
- Adding permanent simplicity, token-budget, line-count, prose-quality, selector, scheduler, cache, or standalone validator machinery.
- Hand-editing generated adapter packages or installed skill copies.
- Rewriting historical review records or package archives.

## Acceptance criteria

| ID | Acceptance criterion | Requirement IDs |
| --- | --- | --- |
| AC1 | Every behaviorally significant current rule has exactly one valid ledger disposition, destination, and governing requirement reference. | R8-R10 |
| AC2 | Universal purpose, authority, checklist, status, finding, recording, proof, stop, claim, handoff, milestone, boundary bridge, and load-trigger policy remains inline. | R2-R4, R6 |
| AC3 | Exactly one mapped `workflow-managed-automated-review.md` reference owns only the automation procedure allowed by R5. | R4-R6 |
| AC4 | Direct and isolated review is complete from `SKILL.md` without loading the automation reference. | R2, R3 |
| AC5 | The mapped assets are the only full copy-and-fill output structures and own no policy. | R7 |
| AC6 | Every identified duplication cluster has one owner and the common path is materially smaller without semantic loss. | R11-R13 |
| AC7 | All required common-path, conditional-reference, total-package, duplication, template, and resource measurements are recorded separately. | R14 |
| AC8 | Static fixtures cover all seven required scenario classes with explicit required and forbidden outcomes. | R15, R16 |
| AC9 | Independent semantic review covers every criterion in R17 and approves the package and ledger. | R17 |
| AC10 | No implementation, validation, verification, release, or acceptance step executes or grades a target agent. | R18, R20 |
| AC11 | Existing deterministic owners validate structure, resources, placeholders, narrow claims, inventory, and package parity without a new validator family. | R19-R22 |
| AC12 | Review vocabulary, severity, recording, settlement, milestone, handoff, downstream authority, and historical evidence remain unchanged. | R23 |
| AC13 | A recorded architecture assessment resolves applicability before planning. | R24 |
| AC14 | Canonical and generated package rollout and rollback preserve a complete, self-contained package at every accepted boundary. | R21, R22, R25 |

## Open questions

None.

The plan must inventory exact existing command owners and decide milestone placement, but those execution details do not alter this contract.

## Next artifacts

- Formal spec review.
- Recorded architecture assessment.
- Architecture and architecture review when the assessment is `architecture-required`.
- Execution plan and plan review.
- Test specification and test-spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.
The package ownership, inline and conditional policy boundary, acceptance proof classes, semantic-preservation ledger, measurements, compatibility, failure behavior, and architecture-assessment obligation are fully specified.
