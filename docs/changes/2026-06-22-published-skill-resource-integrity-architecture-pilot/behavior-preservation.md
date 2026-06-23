# Architecture Behavior Preservation

## Status

active

## Scope

This evidence records M3 behavior preservation for the architecture skill
resource normalization.

M3 changes only the packaging shape of architecture skill-local resources:

- legacy root `templates/...` references are removed from
  `skills/architecture/SKILL.md`;
- earned copy-and-fill or copied-material resources are added under
  `skills/architecture/assets/`;
- the architecture skill gains an explicit `Resource map`.

No arc42, C4, ADR, architecture-review, lifecycle, fallback, or handoff
semantics are intentionally changed.

## Baseline dependency

M3 depends on the reviewed M1 architecture resource-chain audit:

- M1 code review closed cleanly in `reviews/code-review-m1-r1.md`.
- Clean Codex, Claude, and opencode target installations were inspected.
- The first divergent layer was canonical skill source.
- The defect predates package assembly.
- No baseline layer was unproved.

This satisfies the plan requirement that architecture resources change only
after canonical-to-installed baseline evidence is complete.

## Resource classification

| Original source | New skill-local resource | Classification | Reason |
| --- | --- | --- | --- |
| `templates/architecture.md` | `skills/architecture/assets/architecture-skeleton.md` | `assets/` | Copy-and-fill architecture package skeleton with repository lifecycle metadata and all arc42 headings. |
| `templates/adr.md` | `skills/architecture/assets/adr-skeleton.md` | `assets/` | Copy-and-fill ADR skeleton with required ADR fields. |
| `templates/diagram-styles.mmd` | `skills/architecture/assets/diagram-styles.mmd` | `assets/` | Literal Mermaid class definitions copied into flowchart or graph diagrams. |

No `templates/` skill-local resource class was added. No `references/`
resource was added because the inspected diagram material is copied Mermaid
source, not prose guidance.

## Preservation matrix

| Surface | Baseline | New proof | Preservation |
| --- | --- | --- | --- |
| Architecture trigger | `description` and When to Use / When Not to Use require architecture work for multi-component, data-flow, generated-output, deployment, packaging, adapter, quality, security-boundary, or durable-decision changes. | Same trigger wording remains in `SKILL.md`; only resource paths changed. | preserved |
| arc42 sections | `SKILL.md` required canonical `architecture.md` lifecycle metadata plus all 12 official arc42 sections and forbade removing or renaming official sections. | Normative arc42 rules remain in `SKILL.md`; `assets/architecture-skeleton.md` carries the copy-and-fill section scaffold. | preserved |
| C4 diagrams | `SKILL.md` required C4 system context and container diagrams, separate Mermaid `.mmd` source files, optional component/deployment diagrams, and propagation rules. | C4 obligations remain in `SKILL.md`; only the style source changed from missing root template path to `assets/diagram-styles.mmd`. | preserved |
| ADR structure | `SKILL.md` required ADRs for durable architecture decisions and required title, status, context, decision, alternatives considered, consequences, and follow-up. | ADR trigger and required-field wording remains in `SKILL.md`; `assets/adr-skeleton.md` carries the copy-and-fill structure. | preserved |
| Architecture review | `SKILL.md` still hands successful workflow-managed architecture completion to architecture-review when that review is next mandatory or triggered. | Workflow handoff behavior section is unchanged. | preserved |
| Handoff | `SKILL.md` still blocks unresolved design questions and does not imply architecture-review to plan autoprogression. | Handoff wording is unchanged. | preserved |
| Runtime fallback | Missing-resource fallback policy is governed by the skill-contract amendment and package validation; M3 does not broaden runtime fallback. | The architecture package now validates its mapped resources, so fallback is no longer required for the normalized resources. | strengthened |
| Resource availability | Baseline canonical architecture skill referenced missing `templates/...` files outside the skill root. | Canonical architecture skill maps `assets/architecture-skeleton.md`, `assets/adr-skeleton.md`, and `assets/diagram-styles.mmd`; all files exist inside the skill root. | strengthened |
| Generated package parity | Baseline parity for mapped architecture resources did not exist because the architecture resources were unmapped and absent. | M3 creates the canonical mapped-resource source for M4 generated, adapter, archive, and install parity validation. | strengthened |

## Normative-content boundary

The following behavior-significant rules remain in `SKILL.md`:

- when architecture is required;
- upstream status settlement;
- architecture surface decision routing;
- artifact placement lookup order;
- arc42 obligations;
- C4 obligations;
- ADR triggers and lifecycle expectations;
- authoring rules;
- evidence collection expectations;
- workflow handoff behavior;
- stop conditions for unresolved direction, spec, or design questions.

The added resources contain only skeleton headings, field labels, placeholders,
short fill instructions, or copied Mermaid style definitions.

## Removed or rewritten wording

| Previous wording | Replacement | Safety rationale |
| --- | --- | --- |
| `Use templates/architecture.md for the full 12-section arc42 structure.` | `COPY assets/architecture-skeleton.md` in `## Resource map`; `Use the architecture skeleton for section structure.` | The exact skeleton now exists in the skill root and is validated as a mapped asset. arc42 obligations remain normative in `SKILL.md`. |
| `Use templates/diagram-styles.mmd for Mermaid flowchart or graph C4 role styles.` | `COPY assets/diagram-styles.mmd` in `## Resource map`; C4 guidance now says to copy the asset or an explicitly equivalent block. | The copied Mermaid style material is packaged with the skill. C4 diagram obligations remain normative in `SKILL.md`. |
| `Use templates/adr.md and store real ADRs under docs/adr/.` | `COPY assets/adr-skeleton.md` in `## Resource map`; ADR trigger wording says to use the ADR skeleton and store real ADRs under `docs/adr/`. | The ADR field structure now exists in the skill root. ADR triggers and required fields remain normative in `SKILL.md`. |

## Verification expectation

M3 validation covers this evidence with:

```sh
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/behavior-preservation.md
```

M4 and M5 own generated, archive, and clean-install parity for these mapped
resources.
