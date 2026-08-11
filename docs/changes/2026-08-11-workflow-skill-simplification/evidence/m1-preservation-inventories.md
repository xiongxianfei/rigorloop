# M1 Preservation Inventories

Milestone: M1
Plan: `docs/plans/2026-08-11-workflow-skill-simplification.md`
Status: implementation-complete evidence for code review

## Completed scope

- Accounted for 25 behaviorally significant rules or duplication clusters.
- Classified 13 exact literals separately from semantic behavior.
- Added 16 deterministic scenario records covering all seven valid assemblies and distinct invalid, failure, review, and final-review outcomes.
- Added explicit invalid semantic-disposition and literal-classification fixtures.
- Recorded LF-normalized pre-refactor resource and assembly word/byte baselines.

## Decisions

- Universal classification, source precedence, unknown-input behavior, isolation, stop, claim, resource-trigger, and result policy remain inline.
- Lifecycle state interpretation, transition, settlement, milestone, review-resolution, final-review, and closeout procedure move to the governed reference.
- Commands, authorization, bootstrap, automated review gates, receipts, correction, pause, and target completion move to the automation reference.
- Guide creation, refresh, skeleton use, customization, and migration procedure move to the guide reference.
- Tests and snapshots do not become policy owners solely because they reference current headings.

## Unchanged surfaces

- `skills/workflow/SKILL.md`: unaffected in M1 so the baseline is stable.
- `scripts/` and permanent validators: unaffected because M1 evidence is intentionally change-local.
- Generated and installed packages: unaffected because no canonical skill resource has changed.
- Architecture, spec, plan, and test spec: read-only approved inputs.

## Validation

- CMD1: passed; `rules=25 literals=13 scenarios=16 unknown_values=rejected`.
- Change metadata validation: passed.
- Boundary-first feature/proof validation: passed.
- Review artifact structure validation: passed before handoff.

## Handoff

M1 is ready for independent code review. No workflow package prose has moved, and no later milestone has started.
