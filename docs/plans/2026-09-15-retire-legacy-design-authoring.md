# Retire standalone architecture and ADR authoring

## Purpose / big picture

Remove the unsupported standalone architecture/ADR output path as one complete skill, contract and validation change. Preserve engineering meaning, existing project authority and separate feature-spec support.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-15-retire-legacy-design-authoring/change.json).

Mutable activity, work, review, evidence and closeout live in that record.

## Source artifacts

- Proposal: [retirement direction](../proposals/2026-09-15-retire-legacy-design-authoring.md).
- Spec: [Design](../design/skill/authoring/design.md), DES-SR-24 and affected DES-SR-06/13–19/21/23.
- Architecture: DES-DEC-07, public resource map, source disposition and Runtime; [Skill](../design/skill/skill.md) and [System](../design/system.md) delegation.
- Prior-contract test spec: none independently required.
- Exact approved package and review IDs: resolve current proposal-review/design-review-r2 and registered member map through the owning record, without copying mutable approvals into this plan.

## Context and orientation

Canonical sources are skills/, docs/, templates/ and scripts/. Design's complete resource set is validated in scripts/lib/validation/skill_validation.py; tests/skill/test-skill-validator.py contains package, asset, traceability and feature-format checks. The five retired paths are listed in the owning Design with recoverable643f6cd6 provenance. Historical proposals/reviews are evidence, not active source callers; generic template-path lint fixtures test resource boundaries and remain. Inspect sources directly; no project-map currency is assumed.

## Non-goals

No feature-spec/proof retirement, project conversion, existing-document deletion, schema/operation change, unrelated cleanup, active installation, release or publication. No new resource, generic format migration engine or universal automated semantic judge.

## Requirements covered

| Requirement | Allocation | Proof |
| --- | --- | --- |
| DES-SR-24 | M1 supported-output boundary and retirement | TG-01/02, TG-FINAL-01/02 |
| DES-SR-06/13/14/21 | M1 decision/authority preservation | TG-01, TG-FINAL-01 |
| DES-SR-15/17/18/19 | M1 complete package/consumer/closed-resource reconciliation | TG-02, TG-FINAL-02 |
| DES-SR-23 and unaffected shared guards | M1 retained feature resources and ordinary model authoring | TG-01/02, TG-FINAL-02 |

All affected model scenario dimensions map here: input/output and authority to TG-01/F01; composition and compatibility to every group; failure, retry and state-preservation to TG-01/F01; external installed boundaries to TG-FINAL-02. Existing persistence/retry implementation is unchanged and retains its suite protection.

## Milestones

### M1. Retire the complete standalone authoring path

- Milestone kind: implementation.
- Engineering purpose: keep skill selection, available methods, assets and validators coherent in one rollback unit.
- Requirements: all rows above.
- Architecture responsibility: DES-DEC-07 and Design public resources; Assessment retains review authority and Packaging retains generation/install mechanics.
- Dependencies: approved exact proposal and Design packages, independent Delivery Review, user-authorized refinement.
- Implementation scope: remove five exclusive files; reconcile Design body, source-reconciliation, technical/model/governed guidance and Design Review input/output distinction; remove obsolete resource-presence expectations, preserve independent safety/feature checks.
- Files/components likely touched: skills/design/, skills/design-review/SKILL.md, templates/architecture.md, templates/adr.md, scripts/lib/validation/skill_validation.py and tests/skill/test-skill-validator.py; governing evidence. Other reviewer/Plan sources receive an explicit unaffected disposition when they only consume retained inputs.
- Required verification: TG-01/02 and both final integrated groups before milestone review.
- Evidence expectations: complete five-path disposition, surviving obligation mapping, actual independent semantic observations, fail-first package protection, actual supported candidate identities and commands/results.
- Implementation steps: establish retirement and mixed unknown/missing-resource tests before production changes; reconcile the complete skill/consumer slice; remove only exclusive tests and preserve generic path lint, current assets and feature projections; run focused/full/candidate/selected CI; record proof and hand off independently.
- Validation commands: V1–V5 below, V6 for final complete branch.
- Expected observable result: living Design output remains supported, old architecture/ADR requests stop without modifying project files, authorized scoped adoption preserves meaning and old judgment identities, and installed packages omit retired aids while retaining every supported method.
- Completion criteria: all allocated proof passes, independent M1 Code Review approves exact source and compatibility withdrawal, and no required concern remains.
- Required evidence: m1-implementation, m1-validation, m1-candidate and m1-code-review.
- Review handoff: complete actual diff plus approved model/plan, all removed obligations, supported/unsupported paths and generated candidates.
- Optional commit boundary: `Retire standalone architecture and ADR authoring`.
- Risks: accidental feature support removal, implicit project migration, alternate legacy loading, or tests allowing stale resources.
- Rollback/recovery: restore all five files and coupled instructions/resource checks from the recorded base as one coherent unit, preserving evidence and user work; rerun changed proof and independent review.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 and required corrections complete with independent milestone approval.
- Assessment: fresh independent final whole-change Code Review of proposal, Designs, plan, implementation, all consumers and evidence.
- Evidence: exact subjects, nonauthor basis, complete judgment and owned dispositions.
- Successor: distinct final Verify. A one-milestone review or integrated test never substitutes for this checkpoint.

## Change-level verification

### TG-FINAL-01. Supported output and preservation

- Covers: DES-SR-24 and DES-SR-06/13/14/16/21/23.
- Demonstrate: independent nonauthor inspects actual complete revised package using bounded requests for new living Design, standalone ADR amendment with a mandatory local template, architecture rebuild, authorized scoped adoption from a mixed source and retained feature-spec amendment. Name selected resources, expected output/stop, prohibited source mutation, remaining owner, actual surviving instructions and consumer handoff. Required old output stops; authorized adoption maps original requirement/decision identity, rationale, alternatives, consequences and unaffected authority into concrete model fields; incomplete authority stops before write. Confirm Design Review distinguishes source basis from supported output and Plan still consumes relevant retained decisions. Existing real artifacts may support field correspondence; create bounded temporary examples only if necessary. This is semantic/artifact inspection, not claimed live agent compliance.
- Evidence expectations: reviewer, date, exact package/model/asset subjects, observations and limitations in existing review evidence.
- Non-applicability: none.

### TG-FINAL-02. Installed package boundary

- Covers: DES-SR-15/17/18/19/23/24.
- Demonstrate: fresh Codex/Claude candidate build, actual temporary Design clean install, complete current resource parity with declared transforms, absent three retired skill resources, intact feature methods and diagram styles. Repository template copies are absent and no current authored caller loads them; generic fixtures and historical records do not confer runtime support.
- Evidence expectations: actual paths/hashes, commands/results, all current Design resource comparison and independent assessment. No active install.
- Non-applicability: none.

## Validation plan

TG-01 is the complete source obligation map and semantic observation above. TG-02 is independently named retired-resource resurrection rejection plus valid package control, unknown-before-missing consistency check, remaining-resource absence/containment and unchanged feature projection. Preserve full generic path-lint and remaining asset/traceability tests. Removing a retired asset from a no-mutable-state population does not remove the surviving output guarantee.

| ID | Command | Scope |
| --- | --- | --- |
| V1 | `python scripts/validate-skills.py skills` | Complete canonical resource/guidance selection |
| V2 | `python tests/skill/test-skill-validator.py` | Focused changed classes first, then full relevant suite |
| V3 | `python tests/engineering/packaging/test-adapter-distribution.py` | Full supported packaging/installation regressions |
| V4 | `python scripts/build-adapters.py --version v1.0.0 --output-dir DIR`; `python scripts/validate-adapters.py --version v1.0.0 --adapter-root DIR --clean-install-smoke --skill design` | Owned temporary candidate; qualification label, no release |
| V5 | `node scripts/validate-record-store.mjs docs/changes/2026-09-15-retire-legacy-design-authoring/change.json`; `bash scripts/ci.sh --mode local` | Current records and actual changed-set checks |
| V6 | `bash scripts/ci.sh --mode pr --base 643f6cd6d368238f0ca2a5075430634cf9307ad3 --head HEAD` | Complete original-base branch proof, including any selected broad smoke |

Resolve HEAD and DIR to actual immutable revision/path in evidence. After record-only suffixes, validate exact committed owning records; reuse unchanged engineering proof with affirmative content reasoning. Relevant source/candidate changes require refreshed proof. Failed checks stay visible and block dependent claims.

## Risks and recovery

The deliberate compatibility withdrawal must remain explicit in entrypoint, source reconciliation and reviewer guidance. Preserve all existing project files without treating source authority as permission for unsupported output. Publication and installed-package replacement remain separately authorized under their owners.

## Dependencies

No new dependency. Required Python/Node and repository-owned validation/generation tools already exist. Prior authority or proof gaps return to their owning stage before implementation reliance.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-15 | One coupled implementation milestone and separate final review/Verify. | Guidance, resource population and validation must agree in every complete package. | Deleting templates alone leaves live unsupported callers. |
| 2026-09-15 | Keep feature methods, generic lint fixtures and shared styles. | They protect independent supported responsibilities. | Name-based legacy cleanup would remove unrelated behavior. |

## Readiness

See the owning change record for current workflow state. Independent Delivery Review supplies approval of this allocation; this file carries stable intent only.
