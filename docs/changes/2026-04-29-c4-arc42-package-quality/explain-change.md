# C4, arc42, and Architecture Skill Quality Explain Change

## Summary

This change refines the accepted C4, arc42, and ADR architecture package method after the first canonical package exposed quality gaps. It makes the canonical diagrams recognizably C4, strengthens the affected arc42 sections, adds a shared Mermaid C4 style template, tightens architecture authoring and review skills, refreshes generated skill outputs through the existing generators, and records lifecycle/review/verify evidence.

The change remains review-based. It does not add architecture package shape validators, required C4 syntax enforcement, ADR-presence enforcement, new diagram tooling, or generated image artifacts.

## Problem

The repository had the right architecture package shape, but the first canonical package still allowed drift: diagrams could look like generic flowcharts, the Building Block View could become a flat folder catalog, ADR summaries could duplicate decision rationale, and Quality Requirements could remain property lists instead of reviewable scenarios.

The architecture and architecture-review skills also needed sharper guidance so future agents would not repeat those weaknesses while still keeping skills concise.

## Decision Trail

- Proposal: `docs/proposals/2026-04-29-c4-arc42-package-quality.md`
- Spec: `specs/architecture-package-method.md`
- Requirement set: `R76`-`R118`, `AC14`-`AC20`
- Architecture delta: `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md`
- Canonical package: `docs/architecture/system/architecture.md`
- ADR context: `docs/adr/ADR-20260428-architecture-package-method.md`
- Test spec: `specs/architecture-package-method.test.md`
- Plan: `docs/plans/2026-04-29-c4-arc42-package-quality.md`

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `specs/architecture-package-method.md` | Added package-quality contract for diagram source policy, C4 semantics, template expectations, skill content, and review finding format | Make the focused spec own the normative refinements instead of scattering them across workflow prose | proposal direction, spec-review findings | `specs/architecture-package-method.test.md`, lifecycle validation |
| `specs/architecture-package-method.test.md` | Added traceable checks for `R76`-`R118` and `AC14`-`AC20` | Keep requirements testable while preserving review-based first implementation | plan M1-M5 | selector and CI proof |
| `docs/architecture/system/architecture.md` | Refined affected arc42 sections, relative diagram links, building blocks, deployment boundary, ADR summaries, and quality scenarios | Make the canonical package stronger architecture evidence without rewriting every section | architecture review and plan M1/M5 | lifecycle validation and architecture review |
| `docs/architecture/system/diagrams/*.mmd` | Reworked context/container diagrams with C4 role classes, technology labels, and intent-labeled relationships | Make diagrams reviewable as C4 views while keeping Mermaid `.mmd` as the authored source | `R87`-`R95`, `AC15` | manual architecture review and selector routing |
| `templates/architecture.md` and `templates/diagram-styles.mmd` | Added relative diagram-link guidance, separate diagram source guidance, C4 style scaffold, hierarchical building blocks, ADR link summaries, and commented quality-scenario scaffold | Give authors a low-friction starting point that matches the method | `R76`-`R86`, `R105`-`R107` | M1 validation |
| `skills/architecture/SKILL.md` | Kept the skill concise while adding output shape, C4 context/container snippets, ADR triggers, use/skip guidance, diagram policy, and full-file-read guidance | The skill should teach process; templates teach full structure | `R96`-`R104`, `AC18` | skill regression test |
| `skills/architecture-review/SKILL.md` | Added package-quality checks and a simple finding format while preserving the repository material-finding contract | Architecture review must catch C4, arc42, ADR, merge-back, and quality-scenario drift without over-taxonomizing findings | `R109`-`R118`, `AC19` | skill regression test and review artifact validation |
| `.codex/skills/` and `dist/adapters/` | Refreshed generated mirrors through `build-skills.py` and `build-adapters.py` | Generated output must match canonical skill guidance and must not be hand-edited | generated-output boundary, `AC20` | drift checks and adapter validation |
| `scripts/test-skill-validator.py` | Added regressions for architecture and architecture-review skill shape | Make the most important skill-content expectations durable | M2/M3 | `python scripts/test-skill-validator.py` |
| `docs/changes/...` and `docs/plan.md` | Recorded change metadata, architecture delta, code reviews, review resolution, milestone evidence, verify evidence, and plan index state | Keep workflow state durable and reviewable rather than chat-only | workflow contract and active plan | lifecycle, metadata, review-artifact, selector, and CI validation |

## Tests Added Or Changed

- `scripts/test-skill-validator.py` now checks that `skills/architecture/SKILL.md` has the concise C4 + arc42 + ADR output shape, minimal C4 snippets, ADR triggers, use/skip guidance, and full-file-read guidance.
- `scripts/test-skill-validator.py` also checks that `skills/architecture-review/SKILL.md` preserves simple findings while still requiring evidence, required outcome, and safe resolution path or needs-decision rationale for material findings.
- `specs/architecture-package-method.test.md` maps the package-quality requirements and acceptance criteria to manual review checks, selector checks, generated-output checks, and skill regressions.

## Verification Evidence

Verify passed on 2026-04-29 with the full changed-file set:

- `python scripts/select-validation.py --mode explicit ...` returned `status: ok` and selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit ...` passed the selected checks.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-c4-arc42-package-quality` passed.
- `bash scripts/ci.sh --mode broad-smoke` passed.
- `git diff --check -- .` passed.

Hosted CI is not yet observed; that belongs to the PR gate.

## Review Resolution Summary

One material code-review finding occurred during M1:

- `CR1-F1`: accepted by correcting the touched plan readiness and lifecycle wording so the current workflow handoff was accurate.

The finding is closed in `docs/changes/2026-04-29-c4-arc42-package-quality/review-resolution.md`. M2, M3, M4, and M5 code reviews were `clean-with-notes` with no material findings.

## Alternatives Rejected

- Do not add package-shape or required C4 validators in this slice, because the accepted rollout kept first adoption review-based.
- Do not add a component diagram yet, because the refined container view and Building Block View are the first level that needed correction.
- Do not require native Mermaid `C4Context` or `C4Container` syntax, because stable Mermaid flowchart syntax is acceptable when it uses shared C4 role classes.
- Do not put full worked examples into the architecture skill body; keep examples in templates or references to avoid routine token cost.
- Do not duplicate ADR rationale in arc42 section 9; keep section 9 as link-focused summaries.

## Scope Control

- No new architecture method was introduced; this refines the accepted C4 + arc42 + ADR method.
- No generated files were edited by hand.
- No command behavior, selected-check coverage, or validation semantics changed beyond the approved skill regression tests.
- No new dependencies, render pipeline, generated images, or external diagram tooling were added.
- No PR readiness is claimed here; PR preparation remains the next stage.

## Risks And Follow-Ups

- C4 visual sufficiency is still review-based, so future drift depends on architecture-review discipline until a later approved validator exists.
- Component-level validation architecture may eventually deserve its own component diagram, but this change intentionally stops after the refined container view.
- Hosted CI evidence remains for PR stage observation.

## Readiness

- `implement`, `code-review`, `verify`, and `explain-change` are complete for this change.
- The branch is `branch-ready` from verify evidence.
- The next repository stage is `pr`.
