<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Retire the Standalone Test-Spec Stage

Stage: explain-change

Status: current

Final diff identity: `origin/main@7ff73122f72a863bc0ea2619988ef90b84005b1c...4537cb9d8472971a766480889a4ff1aa1528c1df`

Final review identity: `code-review-pr-amendment-r1` recorded by `b62fd0b17b0fd4384b83fdb3f0ac4e9ddbfecd3a`

## Summary

RigorLoop now gives verification ownership to the artifacts that already own behavior and delivery work. The specification defines what must be demonstrably true; the plan allocates requirements and architecture responsibilities to engineering-led milestones and states milestone-level and change-level verification expectations; Delivery Review approves implementation sequencing and verification adequacy together. New governed changes use lifecycle contract v2 and proceed from plan directly to a plan-only Delivery Review package without a standalone test-spec artifact, stage, authoring skill, or review skill.

Historical records are not rewritten. A frozen activation manifest binds each pre-activation change to its exact v1 or legacy-unversioned class. Manifest-bound v1 work that had already passed Delivery Review can continue through common downstream stages, while pre-gate work, unknown values, mixed packages, active retired state, and mismatched manifest identities fail closed.

## Problem

The standalone test-spec stage duplicated relationships already owned by the specification and plan: observable behavior and important scenarios lived in the specification, while allocation, sequencing, completion criteria, and delivery readiness lived in the plan. Maintaining a third artifact forced SR-to-scenario-to-milestone-to-test coverage to remain synchronized across overlapping documents, added a lifecycle gate, and repeatedly loaded similar context. The required assurance was pre-implementation knowledge of what must be verified, where it is allocated, and what evidence implementation must produce—not the existence of `test-spec.md`.

## Decision trail

- The incoming proposal direction became the accepted proposal at `proposal-review-r3`, preserving verification rigor while retiring the standalone lifecycle surface.
- Design Review `design-review-r2` approved the exact design package: architecture `architecture`, specification `spec`, and ADR `adr-verification-ownership`.
- The architecture selected explicit lifecycle contract v2 plus a frozen activation manifest, avoiding inference from dates, artifact presence, Git history, or network state.
- Delivery Review `delivery-review-r3` approved the exact legacy-path delivery package containing `plan` and `test-spec`. The test specification is historical authority for implementing this transition; it is not a template for new v2 changes.
- M1-M5 implemented contract classification, dual lifecycle behavior, verification-ownership redistribution, preactivation parity, and atomic activation. Each implementation milestone has recorded evidence and a clean closing Code Review.
- Final holistic Code Review `code-review-final-r1` reviewed the complete M1-M5 base-to-subject diff and found no material cross-milestone issue.
- Verify R1 then found one stale boundary-first projection: active ownership still named the removed test-spec package. Correction `e84f1fe7` removed that active consumer, preserved historical grandfathering, and made projection failure tests derive their coverage positions from the live inventory. Code Review `code-review-final-r2` found the bounded correction clean.
- The submitted PR exposed recurring local `packages/rigorloop/node_modules/` status noise. Amendment `4537cb9d` added the repository-wide `node_modules/` ignore convention while keeping `package-lock.json` tracked; `code-review-pr-amendment-r1` found the isolated change clean.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| Lifecycle runtime and schema | Added explicit v1/v2 classification, the activation manifest, contract-specific stages, artifacts, packages, corrections, and new-change defaults. | Make the cutover deterministic, preserve exact prior-contract compatibility, and reject mixed or unknown authority. | RTS-R17-RTS-R23; ADR verification ownership | M1 and M2 evidence; TS-001-TS-006, TS-014, TS-015 |
| Specification guidance | Requires observable normal, negative, failure, boundary, compatibility, migration, concurrency, recovery, and authority behavior where relevant, without prescribing test mechanics. | Keep SR-level behavior with the system contract it validates. | RTS-R3-RTS-R5; RTS-AC2 | M3 evidence; TS-007, TS-010 |
| Plan guidance and assets | Requires SR and architecture allocation, engineering-led milestones, lightweight TGs, evidence expectations, and separate change-level verification. | Make the plan the complete delivery contract without recreating a test-spec hierarchy. | RTS-R6-RTS-R12; RTS-AC3, RTS-AC5 | M3 evidence; TS-008, TS-017 |
| Plan-owned specialist references | Added conditional guidance for boundaries, state machines, concurrency, migration, recovery, security, integration, and manual or operational evidence. | Preserve specialist testing methodology with proportional context loading. | RTS-R12; RTS-AC6 | M3 and M4 evidence; TS-009 |
| Delivery Review | Changed v2 membership to one exact primary plan and reviews implementation and verification readiness together; exact v1 packages remain registered compatibility data. | Consolidate the pre-implementation readiness decision without weakening independent challenge. | RTS-R13-RTS-R16; RTS-AC4 | M2 and M3 evidence; TS-003, TS-011 |
| Canonical skills and workflow guidance | Removed standalone test-spec and test-spec-review entrypoints and active routes; retained only explicit historical or manifest-bound compatibility statements. | Reduce lifecycle ceremony and prevent removed authority from being recreated through a sibling path. | RTS-R1, RTS-R2, RTS-R17, RTS-R20 | M4 and M5 evidence; TS-004, TS-012, TS-013 |
| Validators, automation, templates, and adapters | Made closed vocabularies contract-aware, added unknown and mixed-package rejection, and required canonical/generated/archive inventory parity. | Ensure every executable and published surface activates as one coherent package. | RTS-R18, RTS-R19, RTS-R22, RTS-R23; RTS-AC7, RTS-AC10 | M4 and M5 evidence; TS-012-TS-016 |
| Boundary-first resource projection | Removed the retired test-spec consumer from active resource ownership and activation identities, updated consolidated-gate fixtures, and preserved historical grandfathering. | Resolve Verify finding RTS-VRF1 without recreating the retired route or rewriting history. | RTS-R18, RTS-R19, RTS-R23; RTS-AC10 | TS-012, TS-013, TG-FINAL-03; Code Review R2 |
| Local dependency hygiene | Added the root `node_modules/` ignore rule while preserving the tracked package lockfile. | Remove recurring contributor status noise from generated dependency installations. | Repository housekeeping | Direct ignore and tracked-lockfile proof; PR Amendment Code Review R1 |
| Governance and project framing | Updated Vision, Constitution, AGENTS, README, workflow docs, and the Lightweight Requirement-to-Delivery Model. | Align standing project intent and contributor guidance with artifact-independent verification traceability. | Accepted proposal and RTS-R24, RTS-R25 | Design Review R2 and final Code Review R1 |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| TS-001-TS-006 | Contract classification, v2 route, exact prior-contract reading and continuation, activation blockers, mixed rejection, and recovery boundaries. | unit and integration |
| TS-007-TS-011 | Specification behavior ownership, plan allocation and TG structure, specialist loading, traceability, and unchanged downstream authorities. | contract and integration |
| TS-012-TS-016 | Canonical-to-generated parity, supported adapter inventory, structured diagnostics, closed-vocabulary ordering, and documentation scope. | integration and end-to-end |
| TS-017 | A complete new v2 lifecycle from approved design through plan, Delivery Review, implementation evidence, Code Review, and Verify without test-spec state. | end-to-end |
| TS-018 | Historical records remain readable from a fresh checkout without mutation, regeneration, or network access. | end-to-end |
| TG-FINAL-01-TG-FINAL-04 | Complete-change traceability, prior-contract compatibility, coherent activation/publication/recovery, and preserved downstream authority. | change-level |
| Boundary-first projection regressions | Active inventories omit test-spec consumers, historical records remain grandfathered, and rollback/interruption/input-drift coverage follows the live target count. | integration |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| Focused Node lifecycle tests | 66 passed during final Code Review | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| `python scripts/test-change-metadata-validator.py` | 82 passed during final Code Review | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| `python scripts/test-artifact-lifecycle-validator.py` | 166 passed during final Code Review | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| `python scripts/test-skill-validator.py` and `python scripts/validate-skills.py` | 378 tests passed; 21 canonical skills validated | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| `python scripts/test-adapter-distribution.py` | 154 passed during final Code Review | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| `python scripts/test-build-skills.py` | 8 passed during final Code Review | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| Review-artifact structure, change metadata, and diff checks | passed after final review recording | `09cdc5312795e2ab5792141d27a7f7ef9f11cb85` |
| M5 broad smoke | 12 checks passed at the activation implementation revision | `c67ef259` plus bounded correction evidence through `63a8d13f` |
| Boundary-first reference and activation suites | 28 and 66 passed after the Verify correction | `e84f1fe7aa145d8b56700abb2b1e9699b1b8ee45` |
| Boundary-first projection and validation checks | passed with 11 current projections and exact hashes | `e84f1fe7aa145d8b56700abb2b1e9699b1b8ee45` |
| Canonical skill validation | 378 tests passed; 21 canonical skills validated | `e84f1fe7aa145d8b56700abb2b1e9699b1b8ee45` |
| Adapter distribution | 154 passed | `e84f1fe7aa145d8b56700abb2b1e9699b1b8ee45` |

## Review resolution summary

[Review resolution](review-resolution.md) records ten accepted and resolved material findings: one proposal finding, one Design Review finding, two Delivery Review findings, two M1 findings, two M2 findings, and two M5 findings. Every required same-stage rereview is recorded, both final holistic reviews are clean, and the review log reports no open finding. The resolutions strengthened deterministic compatibility, public validator coverage, complete automation propagation, exact plan identity handling, and removal of stale conditional routes without changing the approved direction.

## Alternatives rejected

- Keeping a mandatory standalone test-spec was rejected because it preserves duplicated ownership and synchronization costs.
- Renaming the artifact to a proof-obligation document or adding another mandatory verification skill was rejected because it recreates the same lifecycle surface.
- Making milestones primarily test-driven was rejected because dependency order, safe intermediate states, migration, reversibility, integration boundaries, and implementation risk remain the primary decomposition forces.
- Requiring one SR per test or defining every concrete test before implementation was rejected because TGs express objectives while Implementation owns mechanics.
- Inferring compatibility from dates, file presence, Git history, or network facts was rejected in favor of an explicit contract and frozen manifest.
- Rewriting or migrating completed historical records was rejected; exact read compatibility is sufficient for historical evidence.

## Scope control

The change does not remove test design, automated checks, manual verification, implementation evidence, Code Review, or Verify. It does not merge specification and plan, prescribe implementation-level test mechanics in the specification, introduce in-place v1-to-v2 migration, publish or release adapters, or modify historical artifacts. The branch also contains the approved Lightweight Requirement-to-Delivery Model prerequisite and one isolated dependency-ignore housekeeping amendment; both are identified in the review trail.

## Risks and follow-ups

- Complex plans may become larger when migration, concurrency, compatibility, security, or cross-system risks are real; conditional plan references limit ordinary context cost.
- Plan quality and Delivery Review judgment now carry more verification responsibility; exact package validation and formal semantic review mitigate structural and semantic gaps respectively.
- Historical compatibility intentionally depends on the frozen activation manifest. Missing, additional, reordered, duplicated, class-mismatched, or mixed entries must continue to fail closed.
- Whole-package rollback is safe only before the first v2 record; after v2 use, recovery requires a forward-compatible correction.
- Hosted CI has not been observed by this explanation. Final local evidence currency, branch readiness, and CI applicability remain Verify responsibilities.

## Workflow handback

Explanation status: current

Explanation basis: `7ff73122f72a863bc0ea2619988ef90b84005b1c...4537cb9d8472971a766480889a4ff1aa1528c1df`; final review `code-review-pr-amendment-r1` at `b62fd0b17b0fd4384b83fdb3f0ac4e9ddbfecd3a`

Validation-evidence cutoff: `b62fd0b17b0fd4384b83fdb3f0ac4e9ddbfecd3a`

Open explain-change blockers: none

Control returned to workflow: yes

Next-stage decision owner: workflow
