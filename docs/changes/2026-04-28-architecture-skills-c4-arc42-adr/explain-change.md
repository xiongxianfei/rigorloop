# Architecture Skills C4 arc42 ADR Explain Change

## Summary

This change adopts one repository architecture method built from C4 diagrams, the official 12-section arc42 structure, and separate ADRs. It adds the focused method spec, first real architecture package, templates, lifecycle-validator compatibility, skill guidance, generated skill and adapter refreshes, and a follow-on plan for legacy architecture lifecycle normalization.

The implementation keeps the first rollout review-based. It does not add required architecture package enforcement for arc42 section presence, C4 diagram files, ADR presence, or package shape.

## Problem

Architecture work in the repository could drift because different changes could use ad hoc diagrams, prose-only design notes, or decision notes with no shared structure. That made it harder to review system shape, runtime and deployment implications, cross-cutting concerns, and durable decision rationale.

The accepted direction was to standardize a lightweight but complete architecture method without forcing every feature to rewrite architecture documentation. The repository needed one living canonical architecture package, optional change-local deltas for architecture-significant work, and ADRs for durable decisions.

## Decision Trail

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Proposal decision:
  - adopt C4 plus official arc42 plus ADRs;
  - keep one canonical architecture package;
  - use change-local architecture deltas only as temporary working artifacts;
  - keep templates under `templates/`;
  - keep first implementation review-based.
- Spec: `specs/architecture-package-method.md`
- Requirement set: `R1`-`R75`
- Architecture:
  - change-local working delta at `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`;
  - canonical package at `docs/architecture/system/architecture.md`.
- ADR:
  - `docs/adr/ADR-20260428-architecture-package-method.md`
- Test spec:
  - `specs/architecture-package-method.test.md`, `T1`-`T15`
- Plan milestones:
  - `M1`: lifecycle-validator compatibility for the new canonical arc42 path;
  - `M2`: templates, governance boundary, and workflow pointer;
  - `M3`: canonical architecture package and merge-back;
  - `M4`: architecture skills and generated output refresh;
  - `M5`: legacy normalization follow-on and final closeout evidence.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md` | records the accepted C4 plus arc42 plus ADR direction, canonical package model, change-local delta lifecycle, template boundary, and deferred automation | make the architecture method decision reviewable before spec and implementation | proposal review, spec `R1`-`R3`, `R59`-`R69` | lifecycle validation, proposal-review outcome |
| `specs/architecture-package-method.md` | defines the normative architecture package method, paths, C4 rules, arc42 rules, ADR rules, lifecycle behavior, non-goals, acceptance criteria, and rollout limits | avoid duplicating the full contract in workflow docs and make future architecture work testable | proposal, `AC1`-`AC13` | lifecycle validation, test spec coverage |
| `specs/architecture-package-method.test.md` | maps `R1`-`R75`, examples, edge cases, and acceptance criteria to tests and manual proof surfaces | prove the first implementation without adding premature architecture package enforcement | spec, plan-review findings | lifecycle validation, final verify |
| `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md` and diagrams | captures the change-local working architecture delta and C4 context/container diagrams | provide reviewable design reasoning before merge-back while keeping it non-canonical after acceptance | spec `R30`-`R43`, `R59`-`R61` | architecture-review, manual diagram review, verify |
| `docs/adr/ADR-20260428-architecture-package-method.md` | records the durable decision to adopt C4, official arc42, ADRs, canonical package, change-local deltas, templates, Mermaid source diagrams, and review-based first adoption | preserve the why separately from the architecture shape | spec `R44`-`R48`, `AC7` | lifecycle validation, ADR review |
| `scripts/artifact_lifecycle_contracts.py`, `scripts/test-artifact-lifecycle-validator.py`, and lifecycle fixtures | add path-scoped compatibility for `docs/architecture/system/architecture.md` and regression fixtures proving legacy architecture validation is not weakened | allow the canonical package to use official arc42 headings without adding package-shape enforcement | spec `R67`-`R72`, plan `M1` | `python scripts/test-artifact-lifecycle-validator.py` |
| `templates/architecture.md`, `templates/adr.md` | add canonical scaffolds for official arc42 architecture packages and ADRs | give contributors a consistent starting point without placing templates in live architecture or ADR directories | spec `R49`-`R55`, `AC8` | manual template heading inspection, lifecycle validation |
| `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md` | declare `templates/` as canonical authored content and add only a stage-level pointer to the focused method spec | keep source boundaries clear and avoid creating two normative architecture-method homes | spec `R1`-`R3`, `R52`-`R55` | selector regression, lifecycle validation |
| `docs/architecture/system/architecture.md` and diagrams | create the canonical architecture package using all 12 official arc42 sections plus C4 context/container source diagrams | make the architecture-method change itself the first real positive example and current baseline | spec `R4`-`R29`, `R59`-`R61` | lifecycle validation, manual arc42/C4 inspection |
| `skills/architecture/SKILL.md`, `skills/architecture-review/SKILL.md` | update authoring and review guidance for C4, all 12 arc42 sections, canonical package, change-local deltas, merge-back, legacy status, ADR completeness, summary/ID reasoning, and full-file-read guidance | make agents use and review the new method consistently | spec `R56`-`R58`, `R73`-`R75` | skill validation, skill regression tests |
| `.codex/skills/` and `dist/adapters/` architecture skill output | refresh generated Codex and public adapter skill copies from canonical `skills/` sources | keep generated runtime surfaces synchronized without hand-editing generated output | governance rules, plan `M4` | `build-skills.py --check`, `build-adapters.py --check`, adapter validation |
| `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` | inventories every current `docs/architecture/` file, classifies each, records rationale, targets, and follow-up work | satisfy the required legacy normalization follow-on without migrating every legacy document in the first implementation | spec `R63`-`R66`, `AC10` | `find docs/architecture -type f | sort`, manual table-row proof |
| `docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md`, `docs/plan.md`, `change.yaml` | track milestones, validation, branch readiness, follow-on plan state, and changed-file evidence | keep lifecycle state and handoff evidence durable rather than chat-only | repository workflow rules, plan policy | change metadata validation, lifecycle validation |

## Tests Added Or Changed

- `specs/architecture-package-method.test.md`
  - `T1` proves workflow routing stays a short pointer to the focused method spec.
  - `T2` proves the architecture template keeps lifecycle metadata and all 12 official arc42 sections.
  - `T3` proves default C4 context/container diagrams are source text and reviewable.
  - `T4` proves change-local architecture deltas remain working evidence, not canonical sources.
  - `T5` proves the canonical package uses the official arc42 shape.
  - `T6` proves this architecture-method change is the first positive example and has merge-back evidence.
  - `T7` proves ADR template and ADR rules cover durable decision behavior.
  - `T8` proves governance and workflow docs declare the templates source boundary.
  - `T9` proves the legacy normalization follow-on inventories and classifies current architecture files.
  - `T10` proves architecture skills teach and review the new method.
  - `T11` proves supported validation routing is exercised.
  - `T12` proves lifecycle-validator compatibility is path-scoped and non-enforcing.
  - `T13` proves the first implementation does not add forbidden enforcement or dependencies.
  - `T14` proves architecture artifacts, templates, diagrams, and ADRs stay publishable and readable.
  - `T15` proves final artifact, generated-output, and lifecycle coherence.
- `scripts/test-artifact-lifecycle-validator.py`
  - adds regression coverage for canonical arc42 path compatibility, path scoping, and non-enforcement of package shape.
- Existing validation suites were used for unchanged but affected behavior:
  - skill validation and skill regression tests;
  - adapter distribution tests, adapter drift checks, and adapter validation;
  - selector regression tests;
  - change metadata validation;
  - artifact lifecycle validation.

The test levels are intentional. Executable tests cover lifecycle compatibility, selector behavior, skill structure, generated-output drift, and adapter package validity. Manual review remains the approved first-slice proof for C4 sufficiency, arc42 package completeness beyond lifecycle compatibility, change-local merge-back, and legacy inventory classification.

## Review And Verification Outcomes

- Proposal review: approved after the arc42 section model, canonical package lifecycle, template boundary, and legacy lifecycle clarifications were incorporated.
- Spec review: approved after lifecycle, workflow-pointer, and first-slice compatibility corrections.
- Architecture review: approved after lifecycle/status consistency corrections.
- Plan review: approved after M5 was tightened to require a populated legacy inventory and classification artifact.
- Code review:
  - status: `clean-with-notes`;
  - result: no blocking or required-change findings;
  - no `review-resolution.md` is required because there were no material findings to resolve.
- Verify:
  - verdict: ready;
  - branch-ready is satisfied for the implemented M1-M5 rollout;
  - hosted CI was not observed from this environment.

## Verification Evidence

Final verification and explain-change proof included:

- `python scripts/select-validation.py --mode explicit --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md --path specs/architecture-package-method.md --path specs/architecture-package-method.test.md --path docs/adr/ADR-20260428-architecture-package-method.md --path docs/architecture/system/architecture.md --path docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/change.yaml`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-select-validation.py`
- `git diff --check HEAD~5..HEAD -- .`
- `find docs/architecture -type f | sort`
- manual proof that every inventory path appears as a table row in `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- `bash scripts/ci.sh --mode broad-smoke`

Broad smoke passed and reported unrelated warnings for older baseline proposal files. Those warnings are unrelated to this change and did not block related artifact lifecycle validation.

## Alternatives Rejected

- Keep current architecture skill guidance and ad hoc diagrams/prose:
  - Rejected because it would not solve architecture drift or decision loss.
- C4 only:
  - Rejected because diagrams alone do not cover runtime, deployment, cross-cutting concerns, risks, and durable decision rationale.
- arc42 only:
  - Rejected because prose structure alone does not standardize visual system shape.
- ADR only:
  - Rejected because decisions alone do not explain the current architecture.
- arc42-lite:
  - Rejected after review because the repository chose all 12 official arc42 sections and keeps the package lightweight through concise content plus `Not applicable` rationale.
- Synthetic first example:
  - Rejected because the architecture-method change itself is a stronger real example.
- Template-like files under `docs/architecture/` or `docs/adr/`:
  - Rejected because live artifact directories should not contain disguised templates.
- Required structural validators in the first implementation:
  - Rejected because the package shape needed one real reviewed example before enforcement.
- Immediate full migration of every legacy architecture document:
  - Rejected because the approved spec requires a populated follow-on artifact first, not a first-slice migration.

## Scope Control

- `specs/rigorloop-workflow.md` only gets a routing pointer; the full architecture package contract stays in `specs/architecture-package-method.md`.
- The first implementation adds no required arc42-section, C4-file, ADR-presence, or package-shape enforcement automation.
- No external diagramming, templating, or validation dependency was added.
- Generated `.codex/skills/` and `dist/adapters/` files were refreshed through existing generators, not hand-edited.
- Legacy architecture documents remain in place. The new follow-on plan inventories and classifies them but does not claim they have all been normalized.
- Change-local architecture deltas remain historical evidence after merge-back and must not compete with `docs/architecture/system/architecture.md`.

## Risks And Follow-Ups

- Hosted CI still needs to be observed on the eventual PR.
- The follow-on legacy architecture lifecycle normalization plan remains active and must run later before the repository can claim legacy architecture artifacts are fully normalized.
- Future enforcement automation should wait for a later approved contract after the real package shape stabilizes.
- Future architecture-significant work must keep the canonical package current and add ADRs for durable decisions.

## PR Handoff Summary

- The branch adopts C4 plus official arc42 plus ADRs as the repository architecture method.
- The branch adds the focused spec, test spec, canonical architecture package, ADR, templates, updated architecture skills, generated skill and adapter output, and a legacy architecture normalization follow-on plan.
- The first implementation intentionally stays review-based and adds only narrow lifecycle-validator compatibility for the canonical arc42 package path.
- Local verification passed, including targeted selector/lifecycle/change-metadata proof and broad smoke. Hosted CI has not been observed.

## Readiness

- `explain-change` is complete for this initiative.
- The next stage is `pr`.
- This invocation was a direct `explain-change` request, so no automatic handoff to `pr` was performed here.
