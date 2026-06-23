# Behavior Preservation

Change: `2026-06-23-evidence-bound-incremental-project-map`

Milestone: M3. Representative Output and Preservation Evidence

Status: M3 evidence recorded

## Scope

This evidence covers the canonical `project-map` skill text, packaged skeleton asset, canonical validation enforcement, representative output excerpts, and cold-read proof added through M3.

It does not claim generated adapter inclusion, does not claim final verification, and does not claim branch readiness, PR readiness, or final lifecycle closeout.

## Preservation Matrix

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Orientation-only role | Existing `project-map` skill said it describes what exists today and does not invent future design. | `skills/project-map/SKILL.md` keeps current-state orientation in the opening, workflow-role `must_not_claim`, stop conditions, and downstream reliance sections. | preserved |
| Current-state focus | Existing skill required observed facts and discouraged future design. | Evidence/source-rank rules state that implementation and configuration describe current state, while proposals, specs, architecture plans, ADRs, and execution plans describe intent only. | strengthened |
| Eleven required sections | Existing skill listed eleven required sections. | `skills/project-map/SKILL.md` and `skills/project-map/assets/project-map-skeleton.md` include `Map metadata` plus the existing eleven sections. | preserved |
| Important path citations | Existing skill required file paths for important claims. | The evidence contract requires material current-state claims to cite repository paths and adds material versus incidental examples. | strengthened |
| Observation/inference split | Existing skill required separating observed facts from inferences. | The revised skill defines `observed`, `inferred`, and `unknown`, and requires unknowns to be recorded under `Open questions`. | strengthened |
| Narrow-area support | Existing skill allowed `docs/project-map/<area>.md`. | The revised skill keeps that path, requires durable boundaries, and requires root-map registration. | strengthened |
| Risk routing | Existing skill said risks are orientation and not backlog ownership. | The revised `Follow-up boundary` preserves the prior wording and routes action through owner surfaces rather than execution commitments. | preserved |
| Handoff | Existing skill recommended `explore`, `proposal`, or `architecture`. | The revised skill recommends `explore`, `proposal`, `architecture`, `workflow`, or `none`, and prohibits automatically starting downstream stages during isolated invocation. | preserved and clarified |
| Customer-project mode | Existing skill treated local guidance as optional and avoided RigorLoop originals in customer projects. | The revised `Customer-project orientation` section preserves customer-project wording and portable defaults. | preserved |

## M2 Validation Hooks

- Canonical enforcement runs through `validate_project_map_canonical_contract`.
- `python scripts/test-skill-validator.py -k project_map` covers the valid canonical skill and corrupted canonical copies for missing workflow role, missing skeleton asset, and hidden skeleton policy.
- `python scripts/validate-skills.py skills/project-map/SKILL.md` validates normalized frontmatter, workflow role, resource map, skeleton presence, and canonical project-map contract checks.

## M3 Output Proof

- `docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md` records concise root and area map excerpts for metadata, evidence labels, configured-versus-executed commands, runtime and data-flow evidence, future intent handling, area registration, stale-map handling, correction notes, and placeholder removal.
- `docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md` records small repository, monorepo or multi-service fixture, and intentionally stale map cold-read cases.

## Remaining Proof Owned Later

- M4 owns generated adapter inclusion proof.
