# Execution Plan: Simplify Final Verification and Retire Explain Change

## Purpose / big picture

Replace the standalone `explain-change -> verify` closeout sequence with one impact-aware final Verify stage that generates the durable explanation only on success. The implementation will make `stage-owned-change-local-v3` the sole current executable contract, make the approved Delivery plan the initial evidence map, permit only affirmatively justified reuse of impact-sensitive evidence, preserve policy freshness and always-current checks, keep Verify read-only toward implementation, and publish the new lifecycle only after the complete runtime, governance, skill, validator, adapter, and historical-read package agrees.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-31-simplify-final-verification-retire-explain-change.md`
- Spec: `specs/impact-aware-final-verification.md`
- Architecture: `docs/architecture/2026-08-31-impact-aware-final-verification.md`
- ADR: `docs/adr/ADR-20260831-impact-aware-final-verification.md`
- Approved Design package: `design-review-r1`
- Prior-contract test spec: none; this is a `stage-owned-change-local-v2` change and the approved plan owns verification allocation.

## Context and orientation

The lifecycle runtime is the Node package under `packages/rigorloop/dist/lib/`, with public-path and transaction tests under `packages/rigorloop/test/`. Repository-side lifecycle classification, workflow automation, validation selection, review evidence, schemas, fixtures, and generated-package enforcement live under `scripts/`, `schemas/`, and their test fixtures.

Canonical public skills are authored only under `skills/`. The current `verify`, `workflow`, `pr`, `code-review`, and `ci-maintenance` packages encode the final-stage handoff, while `skills/explain-change/` owns the stage that v3 retires. Current contributor and governance surfaces include `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, affected skill-family specs, templates, adapter metadata, and release validation. Historical proposals, plans, reviews, change records, explain-change artifacts, and release archives remain historical evidence and are not bulk rewritten.

`docs/project-map.md` predates the current v2 consolidated-gate contract and still inventories standalone test-spec ownership, so this plan does not rely on its lifecycle counts or stage topology. The observed runtime and current governed artifacts above provide the bounded orientation basis; project-map refresh is not required to sequence this scoped protocol change.

This change is self-hosting under v2. Implementation may assemble and test a coherent v3 publication candidate, but public v3 activation occurs only after this change and every other nonterminal pre-v3 change is complete or explicitly closed. The last coherent released v2 package remains the bounded authority used for this change's `explain-change -> verify -> pr` closeout. The activated current runtime has no v1/v2 progression branch or compatibility allowlist. Publication or release is not claimed by implementation or Delivery Review.

### Latest-contract simplicity amendment

The current executable product follows one contract: v3. Completed v1/v2 records and release archives remain readable history, not inputs to a current progression checker. M1 and M3 compatibility machinery is an interim preactivation scaffold; M5 removes its executable legacy branches instead of freezing an ongoing v2 allowlist. M4 authors Verify for v3 alone and proves historical readability separately from execution authority.

## Non-goals

- Define a universal semantic dependency graph, exact static impact algorithm, persistent evidence cache, or per-test lifecycle identity.
- Treat filenames, extensions, directories, author assertions, or execution-cache hits as sufficient applicability proof.
- Allow Verify to repair implementation, author plan allocation, settle reviews, choose workflow routing, prepare PR content, or open a PR.
- Remove Code Review, final verification, policy-required broad smoke, hosted CI, security proof, release proof, or environment-sensitive proof.
- Migrate or rewrite completed historical changes, explain-change artifacts, review evidence, or historical release archives.
- Add a replacement explanation stage, explanation skill, evidence-map artifact, test-spec artifact, or standalone impact-analysis skill.
- Hand-edit generated adapter skill bodies or make release publication part of implementation authority.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| FV-R4-FV-R7, FV-R28, FV-R31-FV-R35, FV-R37, FV-R38; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-003, INT-004 | M1 frozen v3 classification, identity, and compatibility foundation |
| FV-R8-FV-R22, FV-R25-FV-R28, FV-R31-FV-R34, FV-R38; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001-INT-003 | M2 impact, applicability, freshness, execution, result, and evidence-tail protocol |
| FV-R1-FV-R3, FV-R23-FV-R34; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002, INT-003 | M3 lifecycle routing, correction ownership, successful explanation, and exact PR handoff |
| FV-R1-FV-R3, FV-R19, FV-R22-FV-R30, FV-R35-FV-R38; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-002-INT-004 | M4 canonical skills, governance, validators, templates, selectors, and generated-package preactivation parity |
| FV-R1-FV-R7, FV-R35, FV-R37, FV-R38; all eight boundary IDs; INT-001-INT-004 | M5 atomic v3 publication candidate and active-entrypoint retirement |
| FV-R7, FV-R22-FV-R34, FV-R37; all acceptance criteria | M6 v2 lifecycle closeout, complete-change evidence, and release-activation precondition |

## Milestones

### M1. Establish frozen v3 classification and compatibility

- Milestone kind: implementation
- Engineering purpose: Add a deterministic v3 contract and preactivation compatibility model before changing current creation or final-stage routing, so every intermediate revision remains serviceable and reversible.
- Requirements: FV-R4-FV-R7, FV-R28, FV-R31-FV-R35, FV-R37, FV-R38; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-003, INT-004.
- Architecture responsibility: lifecycle and compatibility interpreter; frozen pre-v3 v2 inventory; `S -> R -> V` identity boundary; atomic activation and rollback boundary.
- Dependencies:
  - approved Design package `design-review-r1`;
  - current v2 and manifest-bound v1/unversioned readers;
  - existing lifecycle transaction, schema, and activation-manifest behavior.
- Implementation scope: Introduce v3 as an inactive, closed contract; define frozen v2 compatibility evidence and fail-closed classification; preserve current v2 scaffolding and routing until M5. Do not remove the standalone skill or activate v3 in this milestone.
- Files/components likely touched:
  - a v3 activation manifest and schema under the existing lifecycle-contract owners;
  - `schemas/change.schema.json` and lifecycle manifest schemas;
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`, lifecycle readers, status, and new-change fixtures;
  - `scripts/artifact_lifecycle_contracts.py`, `scripts/change_metadata_semantics.py`, lifecycle validators, and focused fixtures.
- Required verification:
  - TG-01 — Classify explicit v3, exact manifest-listed v2, and existing manifest-listed v1 or unversioned records deterministically.
  - TG-02 — Reject unknown contracts, unlisted or class-mismatched v2 records, duplicate or unsorted manifest entries, and v3 records carrying active explain-change state before consistency checks.
  - TG-03 — Preserve historical read-only records and prove no date, filename, artifact-presence, Git, network, or author-asserted heuristic can select a contract.
  - TG-04 — Prove report-tail identities omit self-referential commit identity and remain inactive before v3 activation.
- Evidence expectations: Focused Node and Python regression output showing known classifications, unknown-value failures, exact inventory failures, unchanged v2 new-change behavior, and no mutation of historical fixtures.
- Implementation steps:
  - Add failing classifier, schema, ordering, mismatch, historical-read, and unknown-vocabulary tests first.
  - Add the v3 vocabulary and pure contract classification behind preactivation state.
  - Extend runtime and repository validators through their existing shared boundaries rather than a parallel classifier.
  - Keep v2 as the creation and routing default and record the no-migration rule.
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
- Expected observable result: Runtime and validators understand an inactive v3 contract and exact historical compatibility without changing current v2 workflow behavior.
- Completion criteria: Classification is shared and deterministic; every changed closed set has a named unknown-value regression; v2 remains active; historical records remain byte-unchanged; no migration or v3 entrypoint is exposed.
- Required evidence: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/evidence/m1-v3-classification.md`
- Review handoff: Code Review of contract closure, manifest determinism, identity safety, historical compatibility, and unchanged current routing.
- Optional commit boundary: `M1: add inactive v3 lifecycle classification`
- Risks:
  - A permissive classifier could let unlisted prior records acquire authority.
  - Runtime and Python validators could disagree on the same record.
- Rollback/recovery:
  - Revert the inactive v3 classifier, manifest, and schema additions together; v2 remains the only active contract.

### M2. Implement impact-aware evidence and Verify result semantics

- Milestone kind: implementation
- Engineering purpose: Establish the semantic evidence-selection and final-result protocol independently of public stage retirement, keeping the most safety-sensitive logic reviewable as one bounded slice.
- Requirements: FV-R8-FV-R22, FV-R25-FV-R28, FV-R31-FV-R34, FV-R38; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001-INT-003.
- Architecture responsibility: Delivery verification map; impact classifier; applicability evaluator; freshness classes; always-current set; Verify result and closed evidence tail.
- Dependencies:
  - accepted M1 implementation and Code Review;
  - existing v2 plan verification groups, validation evidence, and Verify report ownership.
- Implementation scope: Define the v3 final-readiness inputs, closed impact/freshness/decision/outcome vocabularies, conservative applicability rules, required execution selection, successful and unsuccessful report shapes, idempotent replay, and tail-drift invalidation. Keep the public v2 graph unchanged.
- Files/components likely touched:
  - `skills/verify/SKILL.md` and new conditional impact/applicability/explanation resources staged for v3;
  - Verify report assets or templates and mapped validator structures;
  - lifecycle validation and change-metadata semantics for Verify results;
  - focused Verify, evidence, cache-separation, and report fixtures.
- Required verification:
  - TG-05 — Resolve exactly one target, governed change, subject, final holistic review, Design package, Delivery plan, and final diff; reject missing, stale, conflicting, or ambiguous identity.
  - TG-06 — Classify every applicable surface as `affected`, `unaffected`, or `unknown`, requiring affirmative non-impact evidence and broadening on uncertainty, including documentation, `.gitignore`, dependency, generated-output, and fixture-controlled cases.
  - TG-07 — Give each required evidence item exactly one freshness class and one `reuse`, `rerun`, or `newly-required` decision; prove fresh-required and always-current obligations override reuse.
  - TG-08 — Distinguish semantic reuse from execution cache hits and require actual execution or observation for rerun, newly-required, fresh-required, and always-current evidence.
  - TG-09 — Prove successful, failed, inconclusive, interrupted, identical-replay, changed-basis, report-write-failure, registration-failure, and tail-drift outcomes, including explanation absence on every non-success.
- Evidence expectations: Direct tests over all closed values and unknown values, normal and negative impact partitions, multi-surface evidence, cache-only attempts, required hosted evidence, report serialization, read-back, registration, replay, and invalid tail changes.
- Implementation steps:
  - Add failing closed-vocabulary, conservative-impact, freshness-override, cache-separation, report-outcome, replay, and drift tests first.
  - Define one normalized evidence-map and result model using existing plan TG and evidence identities; do not add a new governed artifact.
  - Implement deterministic structural checks while leaving semantic non-impact judgment with Verify.
  - Add progressive resources so scoped verification does not load final-impact or explanation procedure.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-validation-cache.py`
  - `python scripts/test-skill-validator.py`
- Expected observable result: Explicit v3 fixtures can produce safe evidence decisions and one complete Verify result, while v2 routing and the standalone explanation stage remain active before cutover.
- Completion criteria: Every evidence obligation has traceable surface, freshness, decision, rationale, and proof; uncertainty never narrows; non-success never contains final explanation or readiness; invalid tail drift stales the result; unknown values fail first.
- Required evidence: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/evidence/m2-impact-evidence-protocol.md`
- Review handoff: Code Review of applicability safety, freshness precedence, cache separation, report truthfulness, identity closure, and read-only ownership.
- Optional commit boundary: `M2: add impact-aware verify evidence protocol`
- Risks:
  - Structural rules could masquerade as semantic impact proof.
  - A report model could accidentally grant readiness from partial or cached evidence.
- Rollback/recovery:
  - Revert the inactive v3 evidence/report additions as one unit; retain M1 only if no v3 result path is exposed.

### M3. Implement v3 routing, correction ownership, and PR consumption

- Milestone kind: implementation
- Engineering purpose: Connect the v3 evidence protocol to lifecycle and PR boundaries without mixing it with broad publication-surface edits.
- Requirements: FV-R1-FV-R3, FV-R23-FV-R34; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002, INT-003.
- Architecture responsibility: v3 stage graph; Workflow routing authority; owner correction and rereview loop; Verify `branch-ready`; exact PR consumption.
- Dependencies:
  - accepted M2 implementation and Code Review;
  - existing lifecycle request, transaction, correction-route, workflow automation, and PR readiness boundaries.
- Implementation scope: Add the inactive v3 `code-review -> verify -> pr` route, remove an explain-change prerequisite from v3, route blockers to exact owners without Verify repair, and make PR consume the current successful Verify explanation and basis. Preserve the released v2 package during preactivation; its runtime branches are removed from the current package in M5.
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`, lifecycle stage routing, read context, operations, and status;
  - `scripts/workflow_automation.py`, `scripts/workflow_automation_policy.py`, `scripts/workflow_automation_state.py`, `scripts/workflow_code_state.py`, and `scripts/lifecycle_state_sync.py`;
  - `skills/workflow/`, `skills/pr/`, `skills/code-review/`, and `skills/ci-maintenance/` contract-keyed guidance;
  - public-path lifecycle, automation, code-state, and PR fixtures.
- Required verification:
  - TG-10 — Prove v3 has no explain-change stage, artifact, prerequisite, transition, correction destination, or automation target; historical v2 evidence does not grant current progression.
  - TG-11 — Route specification, architecture, plan-allocation, implementation, review, CI/environment, and evidence-acquisition blockers to their owners without Verify mutation or silent continuation.
  - TG-12 — Re-enter Verify after correction and rereview, reconsider every evidence item, and preserve only affirmatively current evidence.
  - TG-13 — Prove Verify alone owns `branch-ready`, Workflow alone owns routing, and PR alone owns PR-body/opening readiness.
  - TG-14 — Prove PR consumes the exact successful Verify report and rejects stale, mismatched, incomplete, competing-rationale, or newly referenced authoritative inputs.
- Evidence expectations: Public request-path and automation matrices for v2 and v3, owner-correction fixtures, no-repair assertions, exact report identity checks, and PR negative-path results.
- Implementation steps:
  - Add v3 route and forbidden-stage tests before changing route selectors.
  - Key read and mutation behavior by the resolved contract and reuse existing transaction operations.
  - Update correction and automation policies without granting Verify route or repair authority.
  - Bind PR readiness to one current successful report and forbid competing authoritative rationale.
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-transaction.test.js`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-workflow-automation-policy.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-workflow-code-state.py`
  - `python scripts/test-review-artifact-validator.py`
- Expected observable result: Inactive v3 fixtures route directly from final review and triggered stages to Verify and then PR, with exact owner correction and no leakage into v2.
- Completion criteria: Runtime reads and mutations agree on the v3 graph; every owner route is direct and fail-closed; PR accepts only current successful Verify authority; released v2 evidence remains unchanged and non-current.
- Required evidence: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/evidence/m3-v3-routing-and-pr.md`
- Review handoff: Code Review of graph closure, dual-contract isolation, correction authority, replay behavior, and exact PR consumption.
- Optional commit boundary: `M3: connect verify to v3 routing and PR`
- Risks:
  - Read-side and mutation-side stage graphs could diverge.
  - Compatibility code could expose a retired stage to a new v3 change.
- Rollback/recovery:
  - Revert v3 routing, automation, and PR bindings together; inactive evidence semantics may remain only if they expose no public authority.

### M4. Assemble canonical governance, skill, validator, and adapter parity

- Milestone kind: implementation
- Engineering purpose: Make every staged authored and generated surface express one coherent v3-only package before the activation slice removes the old public entrypoint.
- Requirements: FV-R1-FV-R3, FV-R19, FV-R22-FV-R30, FV-R35-FV-R38; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-002-INT-004.
- Architecture responsibility: progressive Verify package; current-versus-historical inventory; canonical-to-generated package boundary; governance and validator coherence.
- Dependencies:
  - accepted M3 implementation and Code Review;
  - stable v3 runtime, result, and route contracts;
  - canonical skill resource maps and adapter generation pipeline.
- Implementation scope: Update current governance, workflow specs, canonical skills, resources, templates, schemas, selectors, validators, fixtures, adapter metadata, and release checks for v3-only current behavior. Stage explain-change retirement while preserving the last coherent released v2 package and historical archives until M5.
- Files/components likely touched:
  - `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, current workflow and skill-family specs, and relevant architecture indexes;
  - `skills/verify/`, `skills/workflow/`, `skills/pr/`, `skills/code-review/`, `skills/ci-maintenance/`, and staged `skills/explain-change/` retirement inventory;
  - `templates/`, `schemas/`, `scripts/skill_validation.py`, validation selection, lifecycle and review validators, and tests;
  - `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, adapter generation/validation tests, and temporary generated release output.
- Required verification:
  - TG-15 — Inventory current normative surfaces separately from historical evidence and prove all current v3-capable surfaces agree on stage order, owners, evidence reuse, explanation location, and PR handoff.
  - TG-16 — Prove scoped Verify resource loading excludes final-impact and explanation procedure while final readiness loads the complete mapped method.
  - TG-17 — Correct the boundary-first validator's stale v1/test-spec assumptions so v2 plan-only specs validate without weakening boundary structure, and retain explicit unknown-value regressions.
  - TG-18 — Generate and validate Codex, Claude Code, and opencode candidates with no missing resources, escaped canonical paths, mixed inventories, hand-edited bodies, or historical archive mutation.
- Evidence expectations: Closed active-surface inventory, skill validation, boundary validator tests, documentation audit, temporary adapter generation and clean-install validation, parity/drift checks, and proof that historical paths were untouched.
- Implementation steps:
  - Add failing current-versus-historical inventory, resource-loading, boundary-validator, adapter, and mixed-package assertions first.
  - Update canonical governance and skills with v3-only wording and one Verify-owned explanation surface; historical release content is not copied into the current skill.
  - Repair the boundary-first validator to recognize active v2 plan-owned proof without accepting unknown contract values or creating a test spec.
  - Stage adapter descriptors and generate only temporary candidate archives; do not hand-edit generated skill bodies.
  - Keep activation gated on complete parity and the exact pre-v3 change inventory.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/validate-boundary-first.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`
- Expected observable result: A complete v3 candidate can be built and validated from canonical sources while current released v2 and historical evidence remain coherent.
- Completion criteria: Active-surface inventory is closed; validator and skill unknown values fail before consistency; stage-owned plan proof validates through one recursive duplicate-safe YAML parser; all mapped resources resolve; supported generated candidates agree; no historical record or release archive changes.
- Required evidence: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/evidence/m4-v3-package-parity.md`
- Review handoff: Code Review of authority wording, progressive disclosure, validator correctness, canonical/generated parity, and historical scope.
- Optional commit boundary: `M4: assemble impact-aware verify package parity`
- Risks:
  - Active guidance may remain hidden in a template, fixture, or sibling skill.
  - Broad string removal could rewrite historical evidence or valid compatibility fixtures.
- Rollback/recovery:
  - Revert staged canonical, validator, and adapter-descriptor changes together and regenerate temporary candidates from the restored sources.

### M5. Assemble the atomic v3 publication candidate

- Milestone kind: implementation
- Engineering purpose: Switch the current source package to v3 only, retire the standalone entrypoint and executable v1/v2 branches, and assemble one final implementation slice whose complete diff can receive holistic Code Review and v2 closeout before public release activation.
- Requirements: FV-R1-FV-R7, FV-R35, FV-R37, FV-R38; all eight boundary IDs; INT-001-INT-004.
- Architecture responsibility: coherent v3 publication boundary; historical readability without progression; standalone skill retirement; generated package and rollback parity.
- Dependencies:
  - accepted M1-M4 implementations and Code Reviews;
  - every nonterminal pre-v3 change complete or explicitly closed;
  - reproducible canonical and generated parity with no unresolved material findings.
- Implementation scope: Prove the pre-v3 completion gate, switch new-change and active selectors to v3, remove executable v1/v2 compatibility branches, remove `skills/explain-change/` and its current publication entries, update the current adapter manifest and release candidate, and prove the complete local publication candidate. Do not publish, tag, release, or reinterpret historical records.
- Files/components likely touched:
  - v3 activation evidence and current schema/runtime selectors;
  - new-change scaffolding and active lifecycle graph;
  - `skills/explain-change/` removal and current skill inventory;
  - current adapter manifest, release metadata, release validation, and integrated activation fixtures.
- Required verification:
  - TG-19 — A newly scaffolded v3 change reaches final Verify and PR without creating, requiring, routing, or publishing standalone explain-change state.
  - TG-20 — Historical v1/v2 records remain readable without mutation or current progression authority, while non-v3 progression, mismatched, unknown, and mixed records fail closed.
  - TG-21 — Current canonical and generated packages omit standalone explain-change, include complete Verify resources, and reject mixed old/new inventories.
  - TG-22 — Narrow unaffected, unknown-impact, fresh-required, failed correction, interrupted report, tail drift, and exact PR-consumption scenarios pass through public integrated paths.
  - TG-23 — A coherent rollback is possible before first public v3 use; after v3 use, tests reject silent default rollback and require forward-compatible recovery.
- Evidence expectations: Public new-change and final-route fixtures, pre-v3 completion validation, complete package parity, historical-read/non-progression proof, mixed-package rejection, temporary supported-adapter archives, and broad smoke at the reviewed candidate revision.
- Implementation steps:
  - Run the completion and publication prerequisites without mutation and stop on any incomplete prior change or parity gap.
  - Switch current source selectors and new-change scaffolding to v3 while removing v1/v2 progression branches and the standalone authored and published entrypoint in the same slice.
  - Run integrated current-v3, historical-read/non-progression, mixed-package, impact/freshness, correction, report-tail, PR, rollback, and clean-install scenarios.
  - Preserve release publication as an external later action; this milestone creates no release or deployment claim.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-lifecycle-cli-conformance.py`
  - `python scripts/validate-governed-lifecycle-cli.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: The reviewed repository candidate expresses one executable v3 contract, readable non-executable history, one final Verify explanation, and no standalone current explain-change package.
- Completion criteria: Pre-v3 completion, public v3 flow, impact/freshness semantics, correction ownership, closed evidence tail, historical reads without progression, current package retirement, unknown/mixed rejection, generated parity, and rollback boundary all pass at one reviewed revision.
- Required evidence: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/evidence/m5-v3-publication-candidate.md`
- Review handoff: Final implementation-milestone Code Review of activation atomicity, exact compatibility, current entrypoint removal, evidence applicability, identity tail, and generated parity.
- Optional commit boundary: `M5: assemble v3 final verification publication candidate`
- Risks:
  - The cutover could strand an unfinished pre-v3 change or publish one mixed adapter.
  - Removing the canonical skill could be mistaken for permission to skip this change's registered v2 closeout.
- Rollback/recovery:
  - Before public v3 use, restore the last coherent v2 graph, skill inventory, manifest, and generated package together. After v3 use, preserve v3 records and ship a forward-compatible correction.

### M6. Complete v2 lifecycle closeout before release activation

- Milestone kind: lifecycle-closeout
- Engineering purpose: Prove the complete cross-milestone candidate under this change's registered v2 authority, including the final historical `explain-change -> verify -> pr` handoff, before any public v3 release activates the new contract.
- Requirements: FV-R7, FV-R22-FV-R34, FV-R37; FV-AC1-FV-AC14.
- Architecture responsibility: implementing-change v2 completion; final holistic review; exact evidence basis; release-activation precondition without implementation or PR authority leakage.
- Dependencies:
  - M1-M5 implementation milestones closed with required Code Review evidence;
  - no unresolved material findings or open review resolution;
  - complete current-v3 candidate and historical-v2 validation evidence;
  - access to the last coherent v2 skill/runtime package for this record's registered closeout.
- Implementation scope: No product implementation. Assemble final holistic review, current v2 explain-change evidence, final Verify evidence, and PR handoff for this change. Publication, tagging, release, deployment, and post-v3 migration remain outside this milestone.
- Files/components likely touched:
  - `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/explain-change.md` under this record's v2 contract;
  - final holistic review, conditional review-resolution or CI-maintenance evidence, and `verify-report.md` under the owning change root.
- Required verification:
  - TG-24 — Trace every FV requirement and applicable boundary through milestone, TG, concrete proof, reviewed implementation, and current evidence.
  - TG-25 — Re-run integrated v3, historical compatibility, package parity, report-tail, failure/recovery, and exact PR handoff checks against the final reviewed candidate.
  - TG-26 — Prove this change remains v2 throughout closeout and no release-activation evidence predates its successful Verify result.
  - TG-27 — Prove the repository diff contains no mutable lifecycle state in the plan, no unresolved findings, no stale authoritative artifact, and no unsupported hosted-CI or release claim.
- Evidence expectations: Final holistic Code Review receipt, closed resolution when triggered, v2 explain-change artifact, exact commands and results in Verify evidence, lifecycle validators, and PR handoff evidence without release claims.
- Implementation steps:
  - Resolve or disposition every implementation-review finding through its owning stage and required rereview.
  - Run final holistic Code Review over the complete M1-M5 diff and cross-milestone interactions.
  - Invoke the registered v2 explain-change stage from the last coherent v2 package and bind it to the reviewed subject.
  - Run final Verify using the current v2 contract and approved plan commands; prepare PR handoff only if branch readiness passes.
  - Leave any public v3 release to a separately authorized post-completion release action that rechecks the activation preconditions.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-31-simplify-final-verification-retire-explain-change`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/impact-aware-final-verification.md --path docs/architecture/2026-08-31-impact-aware-final-verification.md --path docs/adr/ADR-20260831-impact-aware-final-verification.md --path docs/plans/2026-08-31-simplify-final-verification-retire-explain-change.md --path docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: Current evidence proves the coherent v3 candidate while this change completes its immutable v2 route and makes no premature release or v3 readiness claim.
- Completion criteria: All implementation milestones and reviews are closed; every change-level group passes; v2 explanation and verification are current; PR handoff is authorized by its owner; release activation remains gated on completed pre-v3 inventory.
- Required evidence: Final holistic review receipt, closed review resolution when triggered, v2 explain-change artifact, conditional CI evidence, Verify report, and PR handoff evidence.
- Review handoff: Registered v2 `explain-change`, then `verify`, then `pr`; a separately authorized release action may evaluate v3 activation afterward.
- Optional commit boundary: `closeout: verify v3 publication candidate under v2`
- Risks:
  - A contributor could mistake a validated candidate for a published v3 release.
  - The retired current skill source could obscure the last coherent v2 closeout procedure.
- Rollback/recovery:
  - Keep closeout not-ready, restore or invoke the exact last coherent v2 package for this record, route any defect to its owning milestone, and rerun only invalidated evidence and review.

## Change-level verification

### TG-FINAL-01. Impact-aware final evidence selection

- Covers: FV-R8-FV-R22; M2-M5; BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001; INT-001.
- Demonstrate: The approved plan supplies the initial evidence map; every obligation has a proved surface, freshness class, one applicability decision, rationale, and evidence; affirmative unaffected impact permits reuse; affected or unknown impact broadens; fresh-required and always-current checks run; cache hits never substitute for pass evidence.
- Evidence expectations: Integrated normal, negative, multi-surface, environment, hosted-CI, unknown-value, and cache-separation fixtures plus exact command output.
- Non-applicability: Milestone-local proof is insufficient because the claim spans plan allocation, final diff, policy, prior evidence, and final readiness.

### TG-FINAL-02. Verify outcome, correction, identity, and PR handoff

- Covers: FV-R23-FV-R34; M2-M6; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002, INT-003.
- Demonstrate: Failure and inconclusive attempts have blockers but no explanation or readiness; owner correction and rereview preserve only current evidence; success produces one complete explanation and basis; interrupted, replayed, changed, and drifted tails behave safely; PR consumes only the exact current successful result.
- Evidence expectations: End-to-end public-path lifecycle and report fixtures, final holistic review, replay/drift tests, and PR negative-path evidence.
- Non-applicability: Milestone-local proof is insufficient because the result spans review, correction, Verify recording, lifecycle identity, and PR consumption.

### TG-FINAL-03. V3 activation and historical readability

- Covers: FV-R1-FV-R7, FV-R28, FV-R31-FV-R35; M1, M3, M5, M6; BND-STATE-001, BND-COMPAT-001; INT-004.
- Demonstrate: Current v3 has no standalone stage, skill, or legacy progression branch; historical records remain readable without current authority; non-v3 progression, unknown, mismatched, mixed, and active-explain v3 inputs fail closed; this change completes through the released v2 package before public v3 activation; rollback is coherent only before first v3 use.
- Evidence expectations: Completion-gate validation, current and historical-read fixtures, package inventory checks, current-change closeout identity, and rollback/forward-recovery tests.
- Non-applicability: Milestone-local proof is insufficient because compatibility and activation span runtime, records, skills, schemas, and release publication.

### TG-FINAL-04. Canonical, generated, and validator parity

- Covers: FV-R35-FV-R38; M1-M6; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004.
- Demonstrate: Governance, workflow specs, skills, resources, templates, schemas, validators, selectors, fixtures, adapter metadata, temporary generated packages, and release checks express one v3 candidate; every new closed set rejects unknown values; current mixed packages fail; historical archives remain unchanged.
- Evidence expectations: Documentation audit, lifecycle and boundary validators, skill build checks, supported adapter generation/validation, release-check inventory, broad smoke, and clean diff inspection.
- Non-applicability: Milestone-local proof is insufficient because the publication claim is a cross-component generated-output boundary.

## Validation plan

- Lifecycle Node tests own contract selection, public requests, stage graphs, permissions, report recording, transactions, replay, correction, status, and new-change behavior.
- Repository Python tests own manifest inventory, schema closure, lifecycle and review consistency, workflow automation, code-state interpretation, boundary validation, evidence-selection structure, and unknown-value ordering.
- Skill tests own Verify progressive disclosure, authority and claim boundaries, exact PR consumption, retirement inventory, mapped-resource resolution, and absence of a replacement explanation stage.
- Adapter and build checks own canonical-to-generated parity, supported package inventory, portability, clean-install resource resolution, and drift detection; generated bodies are never hand edited.
- Milestone-focused commands run first. `npm test --prefix packages/rigorloop` expands runtime coverage when the contract is integrated, and `bash scripts/ci.sh --mode broad-smoke` is fresh-required for M5 and M6.
- Hosted CI, release publication, and deployment are not locally claimed. If policy requires hosted observation for PR or release, Verify records it as fresh-required and blocks until observed.

## Risks and recovery

- Risk: Incorrect non-impact classification reuses stale evidence.
  - Recovery: Require affirmative proved-surface reasoning, classify uncertainty as `unknown`, broaden verification, and retain freshness overrides.
- Risk: Verify becomes an oversized public skill.
  - Recovery: Keep universal outcome and authority rules inline and load final-impact and explanation guidance only for final readiness.
- Risk: Runtime, validators, docs, skills, or adapters publish mixed stage graphs.
  - Recovery: Build v3 behind preactivation, close the current-surface inventory, and switch only in the atomic M5 candidate.
- Risk: Historical readability is mistaken for current authority.
  - Recovery: Keep historical paths read-only and reject every non-v3 progression, unknown, or mixed state before consistency checks.
- Risk: The implementing v2 change is stranded or reinterpreted during cutover.
  - Recovery: Complete it through the last coherent released v2 package in M6 and forbid public activation before its closeout; do not add it to current v3 authority.
- Risk: Report self-reference or post-review drift invalidates the reviewed subject.
  - Recovery: Omit report commit identity, register report content, close the allowed evidence tail, and stale any product or governing drift.

## Dependencies

- Accepted proposal, approved Design package `design-review-r1`, and exact primary-plan Delivery Review approval.
- M1 classification precedes v3 semantics; M2 evidence semantics precede routing; M3 routing precedes package authority wording; M4 parity precedes M5 cutover candidate; M6 follows all implementation Code Reviews.
- Each implementation milestone receives direct proof and independent Code Review before its dependent milestone begins.
- M5 blocks unless every nonterminal pre-v3 change is complete or explicitly closed.
- This change remains v2 through M6. Public v3 release activation is a separately authorized action after completion and must recheck inventory, candidate identity, generated parity, and rollback conditions.
- No new test-spec artifact is created. Verification groups in this plan are the v2 Delivery evidence map.
- Generated skills and adapter archives derive from canonical sources and are not hand edited.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-01 | Build v3 behind an inactive discriminator and assemble one atomic publication candidate only after canonical parity. | Reviewable intermediate states must remain coherent and v2 authority must not be silently replaced. | Immediate graph switch; mixed incremental publication. |
| 2026-09-01 | Use plan TGs as the initial evidence map and keep semantic applicability judgment in Verify. | This preserves approved Delivery authority without creating a replacement test-spec or pretending structural validation proves impact. | New evidence-map artifact; per-test identities; filename-only classification. |
| 2026-09-01 | Separate semantic evidence reuse from execution caching. | A cached execution and a durable applicability judgment prove different facts. | Treat cache hits as final pass evidence; rerun every prior check solely because revision changed. |
| 2026-09-01 | Keep this change on v2 through closeout and defer public v3 release activation until afterward. | The approved design forbids reinterpreting the implementing change and requires historical compatibility at cutover. | Self-migrate the in-flight record; activate before final v2 evidence; rewrite historical state. |
| 2026-09-01 | Use six milestones and four change-level groups. | Classification, evidence semantics, routing, publication surfaces, cutover, and closeout have different rollback and review boundaries, while the four integrated claims span them. | One broad implementation milestone; one milestone per file family; milestone-only proof. |
| 2026-09-01 | Keep only v3 executable in the current package; preserve v1/v2 as readable release history. | Historical readability does not justify compatibility branches in every current checker and skill. | Frozen v2 continuation allowlist; contract-keyed current Verify prose; historical migration. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done. Delivery Review must approve this exact primary plan before implementation begins.
