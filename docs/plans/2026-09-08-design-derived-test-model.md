# Deliver the Design-Derived Test Model

## Purpose / big picture

Apply the approved Test criteria through existing specialist skills and demonstrate protection-preserving maintenance on a bounded existing test set. Keep Test criteria distinct from specialist judgments and Review and Closeout policy. Deliver consumer alignment before applying it to cleanup; do not optimize for a deletion count.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-08-design-derived-test-model/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Design-Derived Test Model](../proposals/2026-09-08-design-derived-test-model.md).
- Spec and architecture: unified [Test Design](../design/test/test.md) and [Workflow Design](../design/workflow/workflow.md); no separate specification or ADR is required under the adopted model convention.
- Independent basis: [Proposal Review](../changes/2026-09-08-design-derived-test-model/reviews/proposal-review.json) and [Design Review](../changes/2026-09-08-design-derived-test-model/reviews/design-review.json), including the TEST-SR-03 diagnostic-contribution clarification.
- Governing dependency: [Review and Closeout](../design/review-closeout/review-closeout.md), particularly RC-SR-05–07/11–18.
- Prior-contract test spec: none; rigorloop-records-v2 uses this plan's verification allocation.

## Context and orientation

Canonical skills live in `skills/`; shared contributor-owned sources live in `templates/shared/`. Existing validators and builders own resource parity and generated packages. Installed `.agents/skills/` and private local files are not authored output. Use the primary CLI at `node packages/rigorloop/dist/bin/rigorloop.js` for v2 context, subject inspection and targeted recording. Record Format and CLI remain unchanged dependencies.

Direct inspection of the approved models, relevant canonical skills, builders and selected tests provides the orientation for this policy and test-maintenance scope. No project-map inference is needed. Existing historical Workflow links identified in Design evidence are baseline navigation debt, not authority for this initiative; do not repair them by inventing historical artifacts.

### Consumer allocation

The following closed source families implement the Design inventory. Brace lists denote every named file, not open-ended directory permission. Implementation must enumerate the expanded existing paths in its evidence, identify each changed or unaffected disposition, and inspect the relevant resource-map edges. Newly discovered policy conflicts return to Design. Merely locating an extra file does not authorize a new behavior or an unrelated refactor.

| Source family | Allocated treatment |
| --- | --- |
| `CONSTITUTION.md`, `AGENTS.md`, `specs/rigorloop-workflow.md`, `specs/skill-contract.md`, `docs/architecture/system/architecture.md` | Reference the Test owner for adopted criteria; retain governance precedence, historical contracts, required negative regressions, specialist authority and closeout. Keep internal requirement traceability here. |
| `skills/{spec,architecture,design-review,plan,delivery-review,implement,code-review,verify,route,bugfix,ci-maintenance}/SKILL.md` | Apply only relevant criteria using selective resources. Preserve actual judgment/routing ownership and isolated invocation limits. |
| New `templates/shared/test-quality.md` and `templates/shared/test-maintenance.md` | Portable application text, not competing policy owners. Quality covers derivation, distinct contribution including diagnostics, boundaries, oracles and generated inputs. Maintenance covers retain/strengthen/consolidate/replace/remove, uncertainty, quarantine and discovery impact. No internal IDs or maintainer paths in published text. |
| New `skills/{spec,architecture,design-review,plan,delivery-review,implement,code-review,verify,route,bugfix,ci-maintenance}/references/test-quality.md` | Package quality application for those exact consumers; load only when authoring, allocating or assessing test obligations within the invocation's scope. |
| New `skills/{plan,delivery-review,implement,code-review,verify,route,bugfix,ci-maintenance}/references/test-maintenance.md` | Package maintenance application for those exact consumers; load only when test change/removal or maintenance impact is relevant. |
| `templates/shared/boundary-first-compact-scan.md`, `specs/references/boundary-first-{method,feature-authoring,proof}-v1.md` | Inspect shared criterion overlaps; retain historical format and IDs. Add adopted-profile references or scoping only where needed; do not globally rewrite historical semantics. |
| Existing `skills/{spec,design-review,plan,delivery-review,implement,code-review,verify,route}/references/boundary-first-method-v1.md`; `skills/{spec,design-review}/references/boundary-first-feature-authoring-v1.md`; `skills/delivery-review/references/boundary-first-proof-v1.md` | Keep corresponding packaged copies coherent where their source changes. Preserve specialist boundary methods and avoid loading all resources universally. |
| `skills/plan/references/{boundary-and-negative,state-machine,concurrency-and-retry,migration-and-compatibility,failure-and-recovery,security-and-authority,cross-milestone-integration}-verification.md`, `skills/plan/references/manual-and-operational-evidence.md` | Apply shared criteria where necessary and retain domain methods, allocation and evidence duties. Integrated proof does not substitute for final review. |
| `skills/plan/assets/{plan-skeleton,milestone}.md`; `skills/{design-review,delivery-review,code-review}/assets/review-result-skeleton.md` | Add compact triggered prompts only where existing fields cannot expose test rationale or cleanup evidence. Avoid mandatory per-test records; unchanged assets receive an explicit disposition. |
| `scripts/skill_validation.py`, `scripts/test-skill-validator.py` | Extend the existing shared-resource parity mechanism for selected consumers, with meaningful missing/drift/unknown-consumer regressions. Preserve fail-closed checks. |
| `scripts/build-skills.py`, `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `dist/adapters/{README.md,manifest.yaml}` | Existing generation/validation machinery: inspect and use; change only if integration of the selected resources demonstrates a concrete mechanical need. No new packaging system. |
| `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json`, current candidate entry in `packages/rigorloop/dist/metadata/releases.json`, current candidate digest assertion in `packages/rigorloop/test/cli.test.js` | Regenerate current candidate metadata through existing builder functions when source hashes change; update only its corresponding test expectation. Preserve historical release metadata and version. |

Existing review-assessment/review-reliance resources retain RC policy; no Test criterion is inserted as a new judgment or freshness rule there. The shared requirement-to-delivery explanation retains its many-to-many mapping. Unlisted transitive resources are read for impact; a necessary newly affected file must be allocated by a reviewed plan amendment before editing. No required consumer can be silently deferred past adoption.

### Bounded cleanup set

M2 audits every test method and each parameter/subtest partition in `scripts/test-build-skills.py::BuildSkillsTests` and `scripts/test-boundary-first-validation.py::ModelRecordTests`. The baseline contains 8 and 10 test methods respectively. Method counts identify the audit scope, not a quality target. If the baseline changes before execution, reconcile the exact scope and existing changes before starting.

The first set covers mirror generation, full-resource parity, independent default/output-directory behavior, malformed generated output, and missing/stale resources. The second covers model recognition, supported historical paths, invalid vocabulary/structure, non-applicability, unsafe paths, fenced/indented pseudo-authority, and public read-only validation. This gives concrete opportunities to assess repeated setup, overlapping assertions, diagnostic contribution and helper/public-path distinctions without auditing the whole repository.

Potential consolidation is a hypothesis, not a deletion decision. In particular, direct validator rejection and public-command failure reporting can protect different boundaries. Unknown-value tests, historical path compatibility and read-only public behavior are required protection, even when other tests also reject inputs. Retain unclassified protection. Findings outside these two classes are reported to their owner; they do not expand this cleanup slice automatically.

## Non-goals

- No CLI/schema changes, test ledger, new lifecycle gate, automatic migration, release or customer activation.
- No wholesale test-suite rewrite, deletion quota, blanket removal of slow/flaky/unlabelled tests or changes to production behavior to make tests pass.
- No internal Design IDs or contributor mechanics in published skills.
- No PR opening, push or publication implied by this plan; external handoff requires its own authorization.

## Requirements covered

| Requirement basis | Allocation and evidence |
| --- | --- |
| TEST-SR-01, TEST-SR-02 | M1 TG-01; M2 TG-03 maps each audited group to its actual governing obligation and oracle; missing authority preserves reproduction and routes to Design |
| TEST-SR-03, TEST-SR-04, TEST-SR-05, TEST-SR-06 | M1 TG-01 scenarios for distinct/diagnostic value, boundary, vacuity and randomized proof; M2 TG-03 inspects actual assertion and boundary contributions |
| TEST-SR-07, TEST-SR-08, TEST-SR-09, TEST-SR-10 | M1 TG-01/02; M2 TG-03/04 preserves required detection through maintenance and proves discovery |
| TEST-SR-11, WF-SR-17 | M1 TG-01 ownership and routing; TG-FINAL-01 checks that implemented consumers retain specialist/RC authority |
| TEST-SR-12 | M1/M2 allocations and actual stage evidence; TG-FINAL-01 checks complete bounded scope and honest cleanup claims |
| TEST-SR-13 | M1 TG-02 selective packaging, historical preservation, public portability and governing alignment |
| RC-SR-05–07/11–18 | Evidence applicability, independent milestone/final review, distinct Verify, concern disposition and historical/external limits throughout |

All eight Test boundary rows are allocated: Input domain and Temporal/retry to TG-01/03; State/lifecycle and Failure/recovery to TG-01/03/04; Identity/authority to TG-01 and TG-FINAL-01; Composition/path to TG-01/02/04; Compatibility/migration to TG-01/02/03; External/environment to TG-01/02/04. Workflow's changed Composition/path row and WF-SR-17 map to TG-01 and TG-FINAL-01; unchanged Workflow scenarios retain their original proof obligations.

The three material combined hazards map explicitly: consolidation plus lost public-path protection → TG-01/03/04; flaky sole regression plus missing behavior authority → TG-01; faster validation plus lost discovery → TG-01/04. Synthetic policy cases do not claim that such defects exist in the selected suites.

## Milestones

### M1. Align criteria, consumers and generated packages

- Milestone kind: implementation.
- Engineering purpose: deliver one coherent application of approved criteria before test cleanup depends on it.
- Requirements: TEST-SR-01–13, WF-SR-17; applicable RC policy.
- Architecture responsibility: Test criteria and portable application; specialists retain judgments, Workflow coordination and existing builders packaging.
- Dependencies: approved exact Design and Delivery package; no live work initialization from an unreviewed plan.
- Implementation scope: the consumer allocation above, including selective resource loading, contributor traceability and coordinated candidate metadata.
- Files/components likely touched: the closed consumer allocation; M2 test classes remain unchanged until their audit.
- Required verification: TG-01 semantic policy scenarios and TG-02 package/consumer coherence.
- Evidence expectations: clause-to-consumer dispositions, scenario outcomes, exact subjects, parity/validation results, generated archive identities and historical preservation basis in existing evidence/review records.
- Implementation steps: inspect expanded resource edges; establish focused parity regressions; author shared application and consumers; reconcile governing references; generate and validate supported output; independently review the complete milestone.
- Validation commands: V1–V5 below, plus V8 and V9 for changed model/record surfaces.
- Expected observable result: specialists can derive and maintain useful tests using portable relevant guidance without a second approval authority or internal repository dependency.
- Completion criteria: every allocated source has a coherent changed/unaffected disposition; no required dependency deferred; scenarios and package checks pass; independent milestone Code Review and required corrections complete.
- Required evidence: TG-01/02 results and exact milestone review in the owning v2 record set.
- Review handoff: independent Code Review of all M1 engineering and generated-source interactions.
- Optional commit boundary: `M1: Apply Test model criteria across workflow consumers`.
- Risks: duplicate policy ownership, resource omission, over-broad loading, unintended historical reinterpretation.
- Rollback/recovery: restore the coherent prior candidate guidance/package set; preserve records and historical output. A policy conflict returns to Design before continuing.

### M2. Audit and simplify the bounded test set

- Milestone kind: implementation.
- Engineering purpose: apply the reviewed criteria to real tests with explicit protection-preservation evidence.
- Requirements: TEST-SR-01–05/07–12; historical and diagnostic constraints of TEST-SR-13.
- Architecture responsibility: concrete tests and maintenance rationale; no production behavior or validator-contract changes.
- Dependencies: M1 and its required corrections closed; governing contracts and candidate scope remain current.
- Implementation scope: all methods and subtest partitions in the two named classes, including their shared fixtures/helpers only where required by an authorized consolidation. Other classes remain unchanged.
- Files/components likely touched: `scripts/test-build-skills.py`; `scripts/test-boundary-first-validation.py` within the stated class/helper boundary.
- Required verification: TG-03 maintenance assessment and TG-04 retained detection/discovery.
- Evidence expectations: a compact group-level account covering every candidate, its obligation, violation/boundary/diagnostic value, disposition and remaining protection. Include actual executed checks and any uncertainty; no committed per-test ledger is required.
- Implementation steps: capture baseline discovery and focused outcomes; classify all candidates; establish replacement detection before removing old proof; execute focused tests after changes and surrounding suites; submit maintenance rationale and actual diff to independent Code Review.
- Validation commands: V6, V7, V8 and V9 below. If inspection supports no deletion, run the bounded checks and report the retained-protection rationale without inventing changes.
- Expected observable result: every scoped case has a justified outcome; any simplification preserves supported failure detection and meaningful diagnostic value.
- Completion criteria: the entire bounded set is assessed, required changes completed, unknown protection retained, each removal backed by established remaining proof or explicit governing retirement, discovery checked, and independent milestone review/corrections complete. No minimum count reduction applies.
- Required evidence: TG-03/04 scope and protection comparison, execution provenance and milestone review.
- Review handoff: independent Code Review of actual test changes and all removal/retention claims; a no-change audit still receives scoped independent assessment.
- Optional commit boundary: `M2: Simplify audited tests while preserving protection`.
- Risks: losing public-boundary, unknown-value, historical, side-effect or diagnostic protection; weakening assertions while reducing setup.
- Rollback/recovery: restore the affected tests and fixtures if equivalence fails; retain failing evidence and route missing behavior authority upstream. No quarantine or skip may conceal a gap.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1, M2 and all required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions against the current approved Design and Delivery allocation.
- Evidence: exact final subjects, actual independence basis, judgment, concern dispositions and the relationship between packaged criteria and the cleanup rationale.
- Successor: distinct final Verify. Corrections return to their owner and require affected reassessment; milestone judgments do not substitute for this fresh assessment.

This checkpoint remains mandatory even if M2 retains every test. Verification groups and fresh command runs cannot waive it. Verify alone produces success-only final rationale when its full obligations are satisfied.

## Change-level verification

### TG-FINAL-01. Criteria, cleanup and final evidence agree

- Covers: M1/M2, TEST-SR-01–13, WF-SR-17 and RC-SR-11–15.
- Demonstrate: installed guidance preserves the approved ownership and diagnostic/removal criteria; actual maintenance rationale follows them; every cleanup claim matches the bounded audited set and retained proof; no historical contract, independent review or required discovery check was dropped.
- Evidence expectations: V10 selected integrated validation, current exact model/plan/review/evidence basis, manual comparison of final consumer guidance with TG-03 outcomes, and a distinct final whole-change review followed by Verify.
- Non-applicability: none. Package consumers and maintenance claims cross milestone boundaries.

## Validation plan

### Verification groups

- TG-01: manual semantic assessment of the Test model's eight representative applications plus a useful diagnostic-only case and a renamed-duplicate counterexample. Check all three combined hazards, missing authority routing, randomized reproduction limits, quarantine claim limits and unchanged RC judgment authority. The implementing actor records expected versus observed guidance behavior, exact resource subjects and limitations; independent reviewers assess the result. Keyword tests cannot prove these judgments. Reassess when relevant wording or scope changes.
- TG-02: automated missing/drift/unknown-consumer parity tests, canonical validation, deterministic local mirror and all supported adapter archives. Inspect actual published resources for absent internal TEST/RC/WF identifiers and maintainer-only text. Inspect resource maps to prove maintenance guidance is conditional and unrelated invocations do not load a universal manual. Repeat for changed source/package inputs.
- TG-03: semantic audit of the complete bounded set, with group-level protection comparisons. Explain at least one concrete violating example/failure mechanism for each changed protection group; use focused reproduction or mutation when feasible, without making mutation testing universal. Review actual oracles and bypassed boundaries; different names alone do not justify retention or removal.
- TG-04: baseline and resulting discovered-case comparison, focused tests, and complete surrounding test modules. Account explicitly for each missing/renamed/consolidated case and its subtest partitions; a smaller discovery count alone proves nothing. Verify public-command and helper coverage remain distinct where required. Results expire for reliance when changed tests, runner discovery, relevant fixtures or environment defeat their basis under RC policy.

### Repository-owned commands

| ID | Commands and scope |
| --- | --- |
| V1 | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py` — canonical structure and shared-resource invariants |
| V2 | `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py` — local generation and mirror protection |
| V3 | `python scripts/build-adapters.py --version v0.5.1 --output-dir /tmp/rigorloop-test-model-adapters`; `python scripts/validate-adapters.py --version v0.5.1 --adapter-root /tmp/rigorloop-test-model-adapters` — all supported current candidate archives, without publication |
| V4 | `python scripts/test-adapter-distribution.py` — packaging and metadata compatibility; current candidate metadata must first be regenerated through existing `adapter_distribution` builder functions when source hashes change |
| V5 | `npm test --prefix packages/rigorloop` — CLI/package integration and current-candidate digest expectations; no new command contract |
| V6 | `python scripts/test-build-skills.py BuildSkillsTests -v`; `python scripts/test-boundary-first-validation.py ModelRecordTests -v` — scoped baseline and post-maintenance discovery/results |
| V7 | `python scripts/test-build-skills.py`; `python scripts/test-boundary-first-validation.py` — complete-module validation after M2 changes and before milestone closeout, including surrounding tests affected by shared fixtures or helpers. An unchanged audit may reuse applicable evidence with an explicit RC-SR-15 justification; a result predating a relevant helper or fixture change is insufficient. |
| V8 | `python scripts/validate-boundary-first.py --check --path docs/design/test/test.md --path docs/design/workflow/workflow.md`; `python scripts/validate-markdown-readability.py docs/plans/2026-09-08-design-derived-test-model.md`; `git diff --check` — authoring consistency |
| V9 | `node scripts/validate-record-store.mjs docs/changes/2026-09-08-design-derived-test-model/change.json` — v2 structure and references, not readiness |
| V10 | `bash scripts/ci.sh --mode local --jobs 4` for the final integrated working tree; if preparing an authorized PR, use the existing PR mode with actual full base/head revisions resolved at execution time |

Use focused checks first. Do not run overlapping copies of suites concurrently when they share fixtures. A failed command requires correction or an owned blocker; report failures and skips accurately. RC-SR-15 governs explicit reuse of unaffected existing passes; a new review does not require blind repetition. Run fresh proof for changed tests, resource/package parity, and any expressly freshness-bound check. No hosted CI pass or speed improvement may be claimed without observation or measurement.

## Risks and recovery

- Consumer changes may expose a missing policy decision. Return it to Design and reassess affected approval; do not settle it in a skill or test.
- A test may preserve undocumented regression or diagnostic knowledge. Retain it while investigating; absence of an ID is not evidence of uselessness.
- Shared-resource or candidate metadata changes can leave packages incoherent. Restore or regenerate the complete affected candidate set, keeping historical releases untouched.
- Test reduction can hide discovery loss. Compare case/subtest protection before and after, restore lost proof and rerun the affected checks.

## Dependencies

- The proposal, latest Test Design including diagnostic contribution, Workflow and their independent approvals must remain applicable before reliance.
- Delivery Review must assess this exact plan before implementation or planned-work initialization. Workflow routing remains separately owned.
- M2 depends on M1's reviewed criteria and package coherence. Final review depends on both milestones and corrections; final Verify depends on the fresh final review.
- Record Format/CLI schemas, historical records, external permissions and release versions remain unchanged. Public distribution/customer activation requires separately authorized coherent adoption.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-08 | Align consumers and packaging in one milestone, then audit two bounded test classes | Prevent cleanup from depending on incomplete policy application while keeping the maintenance diff independently reviewable | Mixing arbitrary suite deletion into the policy refactor |
| 2026-09-08 | Audit all 18 baseline methods and their partitions, without a deletion quota | Provide a complete measurable audit boundary while preserving required distinct protection | Repository-wide unbounded audit; judging success by count or runtime alone |
| 2026-09-08 | Keep semantic scenario and maintenance evidence in existing records | Review needs rationale that structural checks cannot supply | New test ledger or assertions mirroring prose implementation |

## Readiness

See the owning change record for current workflow state. Delivery Review, implementation with milestone reviews, required corrections, fresh final whole-change Code Review and successful Verify remain the completion chain. This plan grants no implementation, PR or release approval.
