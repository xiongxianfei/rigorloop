# M2 Route Canonical Cutover Evidence

Milestone: M2
Subject path: docs/plans/2026-09-02-refocus-workflow-into-route.md
Subject identity: sha256:825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d
Validation result: passed

## Result

## Core result

- Skill: implement
- Status: implemented
- Completed scope: Atomically replaced the canonical public workflow skill and guide with the route package and CLI-derived governed context; updated current contracts, governance, architecture, routing consumers, validators, selectors, cache policy, and automation commands; preserved stable workflow protocol state.
- Artifacts changed: canonical `skills/route/`; current governance, architecture, workflow and skill contracts; routing consumers; route/guide, boundary, review, selector, cache, skill, and automation validation surfaces; removal of `skills/workflow/` and `docs/workflows.md`.
- Tests added or updated: route inventory and resource closure, retired-guide authority, CLI-context consumption, portable placement boundaries, `$route` command closure, stored automation continuity, selector coverage, v3 pre-plan spec validation, and clean-review `not-required` handling.
- Validation performed: all ten M2 plan commands plus validation-cache, direct guide alignment, change-local review validation, and `git diff --check`.
- Validation result: all required and additional focused checks passed.
- Open blockers: none.
- Next stage: code-review.
- Claim limitations: M2 does not generate or publish adapters, change installer/release metadata, publish v0.5.0, start M3, establish final verification readiness, or establish PR readiness.

## Planned milestone

- Change ID: `2026-09-02-refocus-workflow-into-route`.
- Plan identity: `docs/plans/2026-09-02-refocus-workflow-into-route.md`, sha256 `825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d`.
- Milestone ID: M2.
- Milestone state: implementation complete and ready for the guarded `review-requested` transition.
- Baseline or change-pack status: exact Design package `design-review-r1` and Delivery package `delivery-review-r1` remain current; M1 is closed after Code Review and M3 remains planned.
- Milestone validation evidence: this file.
- Commit status: prepared for commit `M2: refocus canonical workflow into route` before Code Review.
- Code-review handoff: Review public identity closure, CLI/route responsibility separation, guide removal, stage ownership, automation-state preservation, validator behavior, historical exclusions, and M3 boundaries.

## Scope

- Change: `2026-09-02-refocus-workflow-into-route`
- Milestone: `M2`
- Plan: `docs/plans/2026-09-02-refocus-workflow-into-route.md`
- Plan identity: `sha256:825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d`
- Implementation result: complete

## Canonical cutover

The current authored inventory contains exactly one routing package:

```text
skills/route/SKILL.md
skills/route/references/boundary-first-method-v1.md
skills/route/references/bounded-workflow-automation.md
skills/route/references/governed-lifecycle-routing.md
```

The route identities are:

- `SKILL.md`: `sha256:ae296b81c444817212927e15528b501ee6e62da16197251732d3b06172cc23c7`
- boundary reference: `sha256:4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f`
- automation reference: `sha256:321977b16fcc5fb2b89556310a87215faf3a4f96f185f6231b4a4af38f5c612f`
- governed routing reference: `sha256:32f4e3ddd7345a1505db5e387ae67f6c55d0038f03110f3eaedd6ad53bd1d133`

The canonical `skills/workflow/` package, `docs/workflows.md`, guide-authoring reference, and guide skeleton are deleted together. Historical change records, prior plans, ADRs, and release archives were not rewritten.

## Requirement and verification mapping

| Proof group | Result |
| --- | --- |
| TG-06 | Route-only inventory tests prove the old package and guide-only resources are absent, the three retained references are mapped, and missing conditional resources fail closed. |
| TG-07 | Governed route reads project-phase and exact-change CLI context before semantic routing. Stage skills consume CLI-resolved facts without gaining another stage's authoring or review authority. |
| TG-08 | Existing automation schemas and stored `workflow.automation` state remain unchanged. The automation and state suites cover active, paused, resumable, cancelled, and completed occurrences while the public parser accepts `$route auto:` only. |
| TG-09 | Current governance, workflow and skill contracts, canonical architecture, project map, validator, and selector surfaces use route plus CLI context. The guide validator rejects a current guide or mixed package and ignores a guide only in a historical location. |
| TG-10 | Route and stage guidance distinguish CLI-governed placement from explicit portable defaults; failed governed context cannot fall through to portable placement. |
| TG-11 | Focused regressions allow a v3 spec before primary-plan registration and accept `Resolution: not-required` only for a review with no material or open findings. Existing unknown-value and material-finding checks remain green. |

The stable lifecycle mutation token `stage_authority: workflow` and stored namespace `workflow.automation` remain intentionally unchanged. They are protocol identifiers, not current public skill aliases. The former `$workflow` and `auto-through` public command forms are negative fixtures and no longer execute.

## Current-reference and deletion audit

A bounded scan of `AGENTS.md`, `CONSTITUTION.md`, `README.md`, `docs/project-map.md`, current canonical skills, the current workflow and skill contracts, the automation parser, and cache policy found no current `$workflow`, `skills/workflow`, `docs/workflows.md`, guide-authoring reference, or guide-skeleton dependency. Explicit retirement diagnostics, supersession notices, historical documents, and migration examples remain classified rather than rewritten.

Deleted current surfaces:

- `docs/workflows.md`
- `skills/workflow/SKILL.md`
- `skills/workflow/assets/workflows-skeleton.md`
- `skills/workflow/references/workflow-guide-authoring.md`
- the three retained workflow references at their obsolete paths, replaced byte-for-purpose under `skills/route/references/`

## Validation

All required M2 commands passed on 2026-09-02:

- `python scripts/test-skill-validator.py` — 357 tests passed.
- `python scripts/test-workflow-automation.py` — 78 tests passed.
- `python scripts/test-workflow-automation-state.py` — 70 tests passed.
- `python scripts/test-select-validation.py` — 154 tests passed.
- `python scripts/test-guide-system-validator.py` — 6 tests passed.
- `python scripts/test-boundary-first-validation.py` — 70 tests passed.
- `python scripts/test-boundary-first-reference.py` — 28 tests passed.
- `python scripts/test-review-artifact-validator.py` — 111 tests passed.
- `python scripts/validate-skills.py` — 20 canonical skill files validated.
- `python scripts/build-skills.py --check` — temporary generated-skill parity passed.

Additional focused proof passed:

- `python scripts/test-validation-cache.py` — 25 tests passed after replacing the retired guide in the default policy identity with `AGENTS.md`.
- `python scripts/validate-guide-system.py` — current route and contributor-guide alignment passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-09-02-refocus-workflow-into-route/` — 6 reviews, 5 findings, 6 log entries, and 5 resolution entries passed structural validation.
- `git diff --check` — passed.

## Exclusions and next boundary

M2 does not update adapter descriptors, generated release packages, installer diagnostics, release metadata, or public release claims. Those distribution and migration surfaces remain M3 scope. No external system was mutated and no release was published.

## Code Review R1 correction

Code Review M2 R1 identified two related completeness gaps in the canonical cutover. The correction:

- removes remaining workflow-guide placement fallbacks from current stage skills and uses authoritative CLI context instead;
- deletes the retired guide/map parser constants and callable validation functions from `scripts/skill_validation.py` and retires their active tests;
- consistently names `route` as the semantic routing actor across current skill packages and references while preserving stable protocol identifiers and generic workflow terminology;
- expands `scripts/validate-guide-system.py` across canonical skill Markdown with `ROUTE-GUIDE-009` for semantic guide fallback and `ROUTE-GUIDE-010` for the retired semantic actor;
- adds direct negative fixtures for both prohibited reintroductions and a source regression proving the retired parser cannot return.

The corrected validation results are:

- `python scripts/test-skill-validator.py` — 352 tests passed.
- `python scripts/test-workflow-automation.py` — 78 tests passed.
- `python scripts/test-workflow-automation-state.py` — 70 tests passed.
- `python scripts/test-select-validation.py` — 154 tests passed.
- `python scripts/test-guide-system-validator.py` — 8 tests passed.
- `python scripts/test-boundary-first-validation.py` — 70 tests passed.
- `python scripts/test-boundary-first-reference.py` — 28 tests passed.
- `python scripts/test-review-artifact-validator.py` — 111 tests passed.
- `python scripts/validate-skills.py` — 20 canonical skill files validated.
- `python scripts/build-skills.py --check` — temporary generated-skill parity passed.
- `python scripts/test-validation-cache.py` — 25 tests passed.
- `python scripts/validate-guide-system.py` — current route and contributor-guide alignment passed.
- `git diff --check` — passed.

The correction is ready for Code Review M2 R2. It does not begin M3 or change release scope.

## Handoff

- Review target: M2 canonical cutover and validator changes.
- Requested next stage: `code-review`.
- Branch/PR/release readiness: not claimed.
