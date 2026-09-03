# Execution Plan: Refocus Workflow into Route

## Purpose / big picture

Replace the mixed-purpose `workflow` package with one route-focused public skill, move deterministic project-local workflow facts behind a read-only CLI projection, retire `docs/workflows.md` and its authoring resources, preserve existing v3 automation identity, and publish coherent canonical and generated packages without transferring semantic routing to the CLI.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-09-02-refocus-workflow-into-route.md`
- Spec: `specs/refocus-workflow-into-route.md`
- Architecture: `docs/architecture/2026-09-02-refocus-workflow-into-route.md`
- ADR: `docs/adr/ADR-20260902-route-context-and-skill-identity.md`
- Approved Design package: `design-review-r1`
- Prior-contract test spec: none; v3 uses this plan's verification allocation.

## Context and orientation

The public CLI is the Node package under `packages/rigorloop/dist/`. Command dispatch and rendering live in `dist/bin/rigorloop.js` and `dist/lib/`; focused tests live under `packages/rigorloop/test/`. The existing lifecycle reader already derives current change, artifact, package, milestone, blocker, permission, and automation facts, so the new workflow-context projection should compose those boundaries instead of creating another interpreter.

Canonical skills live only under `skills/`. The current `skills/workflow/` package contains the universal skill, governed routing and automation references, guide-authoring reference, boundary reference, and workflow-guide skeleton. Skill structure, invocation assemblies, placement rules, generated-resource integrity, adapter inventories, validation selection, and guide checks are implemented across `scripts/skill_validation.py`, `scripts/adapter_distribution.py`, `scripts/validation_selection.py`, focused validator scripts, fixtures, and their `scripts/test-*.py` suites.

Current workflow authority is repeated in `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `specs/rigorloop-workflow.md`, `specs/skill-contract.md`, current placement/guide specifications, canonical architecture, templates, and examples. `docs/workflows.md` is currently both the short operational guide and artifact registry. Its retirement therefore requires a coherent canonical cutover rather than deleting the file before CLI defaults, config parsing, stage placement, and validation are ready.

`docs/project-map.md` was last updated before v3 and still describes standalone test specs, explain-change, and `docs/workflows.md` as current. This plan uses direct source inspection for the affected areas and allocates a project-map refresh in the canonical cutover rather than relying on its stale lifecycle topology.

Two existing validators conflict with the current v3 authoring order: boundary validation requires a registered primary plan before Design Review, and detailed clean-review log validation requires a `review-resolution.md` pointer even though current governance says clean reviews need no empty resolution. M2 includes focused corrections and regression proof because final explicit-path validation otherwise cannot demonstrate the approved v3 workflow. No unrelated validator refactor is authorized.

## Non-goals

- Move semantic route selection, blocker interpretation, correction ownership, or automation judgment into the CLI.
- Redesign lifecycle stages, stage-specific artifacts, review authority, `change.yaml`, or existing semantic lifecycle mutations.
- Rename the stored `workflow` authority token or `workflow.automation` namespace.
- Add a workflow daemon, hosted service, external database, executable configuration, or semantic filename inference.
- Preserve `docs/workflows.md` as generated compatibility output or publish a `workflow` alias/tombstone skill.
- Rewrite historical releases, completed records, plans, guides, or archives merely to use the new name.
- Hand-edit generated public adapter bodies or make release publication part of implementation authority.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| RT-R6-RT-R18, RT-R34-RT-R38; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-002, INT-005 | M1 CLI workflow-context, configuration, path safety, output, and non-mutation |
| RT-R1-RT-R5, RT-R10-RT-R12, RT-R19-RT-R29, RT-R33-RT-R38; all eight boundary IDs; INT-001-INT-005 | M2 canonical route/guide/governance cutover, active-run continuity, stage authority, and validator alignment |
| RT-R1, RT-R20-RT-R24, RT-R29-RT-R36; BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-003, INT-005 | M3 generated adapters, stale-install diagnostics, documentation migration, release parity, and historical preservation |
| RT-R1-RT-R38; BND-INPUT-001-BND-ENV-001; INT-001-INT-005 | TG-FINAL-01 through TG-FINAL-03 complete-change proof |

## Milestones

### M1. Add authoritative read-only workflow context

- Milestone kind: implementation
- Engineering purpose: Establish the deterministic CLI/configuration foundation before removing any existing workflow-guide fallback or changing the public skill identity.
- Requirements: RT-R6-RT-R18, RT-R34-RT-R38; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-002, INT-005.
- Architecture responsibility: `rigorloop workflow-context`; bundled defaults; optional `rigorloop.workflow.yaml`; project/change phases; shared lifecycle read model; human/JSON result; safety and non-mutation.
- Dependencies:
  - approved Design package `design-review-r1`;
  - existing lifecycle reader, repository discovery, renderer, and artifact ownership vocabularies;
  - current workflow guide remains authoritative until M2.
- Implementation scope: Add the public read-only command, normalized result model, bundled placement defaults, closed optional config parser, project/change projection, provenance, diagnostics, and tests. Do not rename or delete the current workflow skill or guide in this milestone.
- Files/components likely touched:
  - `packages/rigorloop/dist/bin/rigorloop.js`;
  - new or existing modules under `packages/rigorloop/dist/lib/` for workflow context and configuration;
  - packaged default/config schema metadata under `packages/rigorloop/dist/` and `schemas/` where appropriate;
  - `packages/rigorloop/test/` command, configuration, path, rendering, and lifecycle-composition tests;
  - package README command documentation only where required for the newly callable surface.
- Required verification:
  - TG-01 — Project phase reports lifecycle contract, config provenance, and zero/one/many active candidates without selecting or mutating a change.
  - TG-02 — Change phase reports exact lifecycle revision, stage, artifacts, locations, packages, milestones, blockers, operations, and automation for only the selected change.
  - TG-03 — Bundled defaults and valid overrides resolve deterministically; absent config is valid; empty, unsupported, unknown, duplicate, conflicting, incomplete, absolute, escaped, and symlink-dependent inputs fail closed.
  - TG-04 — Human and JSON output derive from one model, use repository-relative bounded data, and expose no semantic route decision or sensitive host data.
  - TG-05 — Success, failure, ambiguity, interruption, and identical retry leave governed and config files byte-identical; a mutation makes a prior revision stale.
- Evidence expectations: Focused Node tests covering public invocation, both phases, all closed config/result values and unknown values, path containment, candidate ambiguity, multiple permitted transitions, active automation projection, identical reads, byte identity, and output parity.
- Implementation steps:
  - Add failing public-command, project/change phase, closed-vocabulary, unsafe-path, ambiguity, privacy, and non-mutation tests first.
  - Factor or reuse lifecycle interpretation so workflow context has no second transition engine.
  - Add bundled defaults and the closed data-only override parser with provenance.
  - Add human and JSON rendering and package the required defaults/schema.
  - Keep current workflow/guide consumers unchanged until the command passes its complete focused suite.
- Validation commands:
  - `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/workflow-context.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-change-metadata-validator.py`
- Expected observable result: `rigorloop workflow-context` provides deterministic, inspectable, non-mutating project or exact-change facts while the current workflow skill and guide continue to operate.
- Completion criteria: Both phases and every failure class are directly proved; all new closed values reject unknowns before consistency; no test observes a semantic CLI choice or state mutation; existing lifecycle tests remain green.
- Required evidence: `docs/changes/2026-09-02-refocus-workflow-into-route/evidence/m1-workflow-context.md`
- Review handoff: Code Review of CLI authority limits, configuration closure, path safety, lifecycle reuse, output privacy, and byte-identical failure behavior.
- Optional commit boundary: `M1: add read-only workflow context`
- Risks:
  - The new projection could duplicate and drift from the lifecycle interpreter.
  - A permissive template parser could escape the repository or create conflicting ownership.
- Rollback/recovery:
  - Revert the additive command, defaults/schema, and tests as one unit; current workflow and guide behavior remain intact.

### M2. Cut over canonical workflow ownership to route

- Milestone kind: implementation
- Engineering purpose: Perform the compatibility-sensitive source-of-truth transition as one coherent canonical slice so no reviewed commit treats both public skills or both workflow-information sources as current authority.
- Requirements: RT-R1-RT-R5, RT-R10-RT-R12, RT-R19-RT-R29, RT-R33-RT-R38; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-001-INT-005.
- Architecture responsibility: route package; guide retirement; CLI-to-route handoff; stage ownership; portable mode; stable `workflow` protocol role and automation namespace; coherent canonical contract and validation.
- Dependencies:
  - accepted M1 implementation and Code Review;
  - complete current-reference inventory for `skills/workflow`, guide resources, and `docs/workflows.md`;
  - existing automation fixtures representing active, paused, resumable, cancelled, and completed occurrences.
- Implementation scope: Atomically rename canonical `skills/workflow/` to `skills/route/`, remove guide-only files and invocation assemblies, make governed route consume CLI context, remove current `docs/workflows.md`, update all current governance/specification/architecture/template/selector/validator/test/project-map surfaces, preserve portable defaults without governed claims, and retain stored workflow protocol identifiers. Historical artifacts and release archives remain unchanged.
- Files/components likely touched:
  - `skills/workflow/` removal and new `skills/route/` package with retained routing, automation, and boundary resources;
  - `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md` removal, `docs/project-map.md`, canonical architecture, and current docs indexes;
  - `specs/rigorloop-workflow.md`, `specs/skill-contract.md`, current guide/placement contracts and applicable supersession notes;
  - `scripts/skill_validation.py`, `scripts/validation_selection.py`, `scripts/validate-guide-system.py` retirement or refocus, boundary/reference/review/lifecycle validators, and focused fixtures/tests;
  - workflow automation and lifecycle tests only where public skill identity or guide lookup is asserted.
- Required verification:
  - TG-06 — Current discovery exposes only route; guide predicates, assemblies, reference, skeleton, and workflow-map fallback are absent; required routing/automation resources remain exact and fail safe.
  - TG-07 — Governed route calls CLI context and retains semantic selection; stage skills retain their authoring/review boundaries; structural permission and path resolution never transfer authority.
  - TG-08 — Active, paused, resumable, cancelled, and completed `workflow.automation` fixtures keep exact identity, target, budgets, receipts, and state through route with no rename migration.
  - TG-09 — Current governance, specs, architecture, docs, selectors, validators, fixtures, and project map no longer grant `docs/workflows.md` or the public workflow skill authority; a retained historical guide is ignored.
  - TG-10 — Portable explicit/default placement remains safe but cannot claim governed state or project customization; invalid governed context never falls through to portable behavior.
  - TG-11 — Boundary validation permits a v3 spec before plan registration, and clean-review validation accepts no-resolution receipts while preserving every material-finding requirement and unknown-value failure.
- Evidence expectations: Canonical inventory and resource-map checks; route invocation matrix; automation compatibility fixtures; stage-authority negative tests; retained-guide non-authority tests; selector/doc/reference scans; direct regressions for both stale v3 validators; exact deletion inventory and historical exclusions.
- Implementation steps:
  - Add failing route-only inventory, no-guide, CLI-consumption, stage-authority, automation-continuity, portable-boundary, stale-validator, and historical-ignore tests first.
  - Rename and reduce the canonical skill package while preserving routing and automation semantics.
  - Update current governance and normative contracts, explicitly superseding current guide-authority clauses without bulk rewriting history.
  - Remove the guide and refactor or retire its dedicated validators and selection categories.
  - Refresh the project map from direct source evidence and run canonical skill/resource validation before adapter generation.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-guide-system-validator.py`
  - `python scripts/test-boundary-first-validation.py`
  - `python scripts/test-boundary-first-reference.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: Canonical current source has one route skill and one CLI workflow-information authority, no current workflow guide, unchanged stage ownership, and resumable existing automation.
- Completion criteria: Direct current-reference scans find no unauthorized old name or guide authority; every retained `workflow` string is classified as protocol state or history; route package and validators pass; both observed v3 validation-order defects have focused regressions; historical bytes remain untouched.
- Required evidence: `docs/changes/2026-09-02-refocus-workflow-into-route/evidence/m2-route-canonical-cutover.md`
- Review handoff: Code Review of public identity closure, source precedence, guide removal, semantic/structural separation, stage ownership, automation identity, validator preservation, and historical exclusions.
- Optional commit boundary: `M2: refocus canonical workflow into route`
- Risks:
  - Broad text migration could rewrite history or confuse stored workflow protocol names with the retired public skill.
  - Removing guide validators could accidentally remove unrelated source-of-truth or placement checks.
- Rollback/recovery:
  - Revert the complete canonical cutover together to restore the prior coherent workflow/guide package; never restore only the skill or only the guide.

### M3. Publish coherent adapter and migration surfaces

- Milestone kind: implementation
- Engineering purpose: Propagate the reviewed canonical cutover through generated adapters, installation diagnostics, packaging metadata, examples, and release verification, then prove the complete supported distribution boundary.
- Requirements: RT-R1, RT-R20-RT-R24, RT-R29-RT-R36; BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-003, INT-005.
- Architecture responsibility: canonical-to-generated package boundary; obsolete-name diagnostics; historical archive preservation; coherent release unit and rollback.
- Dependencies:
  - accepted M2 implementation and Code Review;
  - canonical route package and current docs/validators are stable;
  - existing adapter generator, manifest, installer, release metadata, and clean-install proof.
- Implementation scope: Update supported adapter descriptors and manifests, installer/upgrade diagnostics, adapter documentation, command examples, token/packaging inventories, release checks, and temporary generated archives for route. Prove no current workflow alias or guide resource is packaged and historical archives are unchanged. Do not publish a release.
- Files/components likely touched:
  - `dist/adapters/manifest.yaml` and `dist/adapters/README.md`;
  - `scripts/adapter_distribution.py`, adapter templates, installer/init checks, release validation, and focused tests;
  - package README and current adapter invocation examples;
  - adapter artifact and token-cost inventory logic where skill paths are closed values;
  - temporary generated Codex, Claude Code, and OpenCode package trees and archives used only as validation output.
- Required verification:
  - TG-12 — Every supported adapter installs and invokes route with the same arguments and mapped resources, and no current workflow package, alias, guide reference, or guide skeleton appears.
  - TG-13 — Installed/mixed/obsolete current workflow packages are diagnosed with route as replacement; compatible active automation state remains readable after upgrade.
  - TG-14 — Canonical, generated, packed, archived-candidate, and clean-install resource inventories and raw-byte identities agree for route.
  - TG-15 — Historical release archives and completed records remain byte-identical; current release checks distinguish history from current package claims.
  - TG-16 — Generation, validation, or install interruption leaves no partially authoritative current package; rerun or rollback returns to one coherent package.
- Evidence expectations: Adapter generator and distribution test output, clean-install trees for all supported adapters, obsolete/mixed package diagnostics, archive inventory and byte-parity evidence, historical hash comparison, release-check dry validation, and exact command examples.
- Implementation steps:
  - Add failing route inventory, obsolete/mixed detection, adapter command, resource parity, interruption, and historical-preservation tests first.
  - Update descriptors, manifests, templates, installer diagnostics, and current documentation from canonical route identity.
  - Generate candidates through repository tooling; never hand-edit adapter bodies.
  - Validate clean installs and archives for every supported adapter and audit remaining old-name/guide matches by current versus historical scope.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/build-skills.py --check`
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: All supported current distributions expose route only, diagnose obsolete workflow installations, preserve historical archives, and pass repository release-oriented validation without publishing.
- Completion criteria: Supported adapters and clean-install proof agree with canonical route resources; mixed and old current packages fail clearly; interruption is recoverable; broad smoke passes; no public release or availability claim is made.
- Required evidence: `docs/changes/2026-09-02-refocus-workflow-into-route/evidence/m3-adapter-and-release-parity.md`
- Review handoff: Code Review of generated parity, install/upgrade compatibility, failure cleanup, historical preservation, release claims, and absence of hand-edited derived output.
- Optional commit boundary: `M3: propagate route through supported adapters`
- Risks:
  - Closed inventories may omit one adapter or documentation entry and produce a mixed public package.
  - Migration diagnostics may accidentally reintroduce workflow as an executable alias.
- Rollback/recovery:
  - Before publication, revert adapter/metadata/documentation changes with the canonical M2 cutover if needed. After any later publication, recover through a corrective release; immutable archives are never rewritten.

## Change-level verification

### TG-FINAL-01. Deterministic context and semantic routing separation

- Covers: RT-R2-RT-R18, RT-R25-RT-R28, RT-R34-RT-R38; M1-M3; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-002, INT-004, INT-005.
- Demonstrate: End-to-end governed routing obtains project and exact-change facts from the CLI, handles candidate/configuration/stale/failure states without mutation or fallback, leaves semantic owner selection with route, preserves stage authority, and resumes exact automation state.
- Evidence expectations: Public CLI plus route integration fixtures, multi-candidate and multi-transition cases, invalid config/path cases, stage-owner negative proof, byte identities across failed reads, and active-run resume evidence.
- Non-applicability: Milestone-local proof is insufficient because the claim crosses CLI, configuration, route semantics, lifecycle mutation, stage handoff, and automation.

### TG-FINAL-02. One current route and workflow-information package

- Covers: RT-R1, RT-R19-RT-R33; M2-M3; BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-002, INT-003.
- Demonstrate: Canonical source, governance, specs, docs, validators, selectors, adapters, installers, generated candidates, and release checks expose route and CLI context only; current workflow alias and `docs/workflows.md` authority are absent; stable protocol/history occurrences are classified and preserved.
- Evidence expectations: Closed current-surface inventory, resource and adapter parity, stale-install diagnostics, retained historical-guide ignore case, historical archive hashes, and no-guide cold-read workflow proof.
- Non-applicability: Milestone-local proof is insufficient because source-of-truth and distribution coherence span canonical, generated, installed, historical, and release surfaces.

### TG-FINAL-03. V3 validation, failure, and recovery integrity

- Covers: RT-R24, RT-R30, RT-R32-RT-R38; M1-M3; all eight boundary IDs; INT-001-INT-005; observed v3 validation-order obligations.
- Demonstrate: Unknown values fail before consistency, clean reviews need no empty resolution, specs validate before plan registration, required route resources fail safe, context is read-only, generation/install interruption does not create partial authority, full lifecycle validation and broad smoke pass, and rollback boundaries remain coherent.
- Evidence expectations: Unknown-value regressions for every new vocabulary, corrected validator fixtures, failure/byte-identity tests, lifecycle validation, exact-path validation, review-artifact validation, build/adapter checks, and fresh broad smoke.
- Non-applicability: Milestone-local proof is insufficient because final integrity spans authoring order, review recording, runtime, filesystem failure, generated packages, and repository governance.

## Validation plan

- Node package tests own workflow-context parsing, public invocation, lifecycle composition, output rendering, path safety, configuration closure, and byte-identical read behavior.
- Python validator tests own route skill structure, current/historical inventory, source precedence, stage authority, automation compatibility, validation selection, clean review receipts, boundary stage order, and unknown-value ordering.
- Adapter tests own canonical-to-generated resource inventory, supported invocation names, clean install, stale/mixed package diagnostics, interruption cleanup, and historical archive preservation.
- Milestone-focused commands run first. `npm test --prefix packages/rigorloop` expands CLI/runtime coverage after integration; `bash scripts/ci.sh --mode broad-smoke` is fresh-required after the complete M3 candidate.
- Final explicit-path lifecycle validation includes the approved spec, architecture, ADR, plan, change record, route skill, workflow configuration/schema surfaces, current governance, adapter manifest, and review evidence.
- Hosted CI, release publication, deployment, and public availability are not implementation or Delivery Review claims. Verify must record any required hosted observation separately.

## Risks and recovery

- Risk: CLI context grows into a semantic workflow engine.
  - Recovery: Keep output candidate-based, add negative tests for multiple allowed routes, and reject any code path that chooses correction meaning.
- Risk: Invalid configuration enables unsafe or ambiguous artifact placement.
  - Recovery: Use a closed data-only schema, repository containment, ownership consistency, explicit provenance, and fail-closed resolution.
- Risk: Canonical cutover leaves one current old-name or guide-authority surface.
  - Recovery: Maintain a closed current-versus-historical inventory and revert M2 atomically if canonical validation cannot agree.
- Risk: Stored `workflow` tokens are accidentally renamed or treated as stale skill packages.
  - Recovery: Classify protocol fields separately, preserve fixture identities, and test active-run resume through route.
- Risk: Adapter generation produces a mixed or partial distribution.
  - Recovery: Generate into temporary output, validate all supported inventories and raw bytes before replacement, and publish only through a later authorized release.
- Risk: Removing guide-specific validators weakens unrelated governance checks.
  - Recovery: Map every retired check to CLI config/context, canonical skill, or explicit obsolete behavior before deletion and preserve negative fixtures at the new owner.

## Dependencies

- Accepted proposal, approved exact Design package `design-review-r1`, and approval of this exact primary plan by Delivery Review.
- M1 precedes guide retirement; M2 consumes M1 and must remain one coherent canonical cutover; M3 consumes the reviewed canonical package.
- Each milestone receives direct proof and Code Review before its dependent milestone begins.
- No standalone test-spec is created. This plan's TG groups are the v3 Delivery evidence map.
- Generated adapters and archives derive from canonical `skills/`; generated bodies are not hand edited.
- Release publication is a later separately authorized action after implementation, Code Review, Verify, and PR readiness.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-02 | Add CLI context before removing guide fallback. | The route package needs an authoritative deterministic replacement before the old source can disappear. | Delete the guide first; let route infer missing facts. |
| 2026-09-02 | Make the canonical rename and guide retirement one implementation milestone. | A reviewed intermediate commit must not expose two current public names or two workflow-information authorities. | Separate rename and guide deletion milestones; long-lived compatibility alias. |
| 2026-09-02 | Preserve stored `workflow` authority and automation namespaces. | They are stable protocol identities, and renaming them adds migration risk without user value. | Rewrite active records; dual stored schemas. |
| 2026-09-02 | Use three implementation milestones and three change-level groups. | CLI foundation, canonical authority cutover, and distribution parity have distinct dependency and rollback boundaries; integrated claims cross them. | One repository-wide milestone; milestones per file family. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done. Delivery Review must approve this exact primary plan before implementation begins.

