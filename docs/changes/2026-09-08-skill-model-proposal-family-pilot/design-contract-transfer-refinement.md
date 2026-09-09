# Common contract transfer refinement

Owning change: [change.json](change.json). This author-owned correction addresses independent finding `skl-dr-001`; its reporter retains disposition authority.

The root cause was treating a topic-level displacement mapping as a complete normative destination. The earlier metadata correction preserved its named examples but left portability and resource enforcement dependent on source prose slated for retirement. The correction now states the applicable population, triggering condition, required outcome and exception/supersession together in Skill.

## Selected transfer check

| Selected common area | Destination and correction assessment |
| --- | --- |
| Metadata, routing, role summary and vocabulary; Skill Contract R3/R29–31 and Readability R11–24/32–35 | Existing retained table defines fields, values, populations and reviewed equivalents. This refinement preserves that prior correction. |
| Portability; Skill Contract R3d–l/R12b/R27b/R32d/R33–c | Added exact public-copy coverage and contributor exclusions, allowed portable surfaces, target/supplied-resource exceptions and distinction between local scripts and repository-root internals. |
| Procedure and evidence; R16–18/R21–26/R31–34 | SKL-SR-03/06–08/12/14 and the retained table cover procedure, selection and output. Added explicit full-subject escape conditions, obtaining omitted detail, example placement and process-finding evidence. |
| Resource declaration and integrity; R47–51 | SKL-SR-08–10 retains classes, containment, presence, identities and transformations. Added recognized legacy loading/prefix scope, arbitrary-path exclusions and unmapped-dependency failure or explicitly approved temporary debt. Legacy templates recognition does not approve a resource class. |
| Enforcement population and fallback; R53–54 | Added immediate new/changed-skill enforcement and clean-audit or review-visible drift-disposition prerequisite for inventory enforcement. SKL-SR-09/11 retains invocation failure/fallback versus package validity. Completed initial audit is historical; active enforcement is not reset. |
| Shared projections, specialist rules and proof history | SKL-SR-04/13 and displacement rows retain specialist owners and exact copied-source responsibilities. Plan assets and boundary methods remain current at their named retained sources. Historical pilot proof requirements remain superseded; this refinement selects no new benchmark or inventory audit. |

This is a bounded author assessment of the selected common transfer, not an inventory conformance audit or independent judgment. It changes only the Skill Design and author-owned recording/evidence; no source is retired and no pilot implementation is performed. SKL-DEC-01–05 retain their decisions. The earlier authoring/correction notes remain snapshots of their original subjects.

Prior reviewed Skill: `sha256:8e551e0ebcb35d7bd165baf5dcc833ff82a266c995eb1e25e80ebc2e0e2aceb2`.

Refined Skill: `sha256:6c15e11c170ba7886439ba6db6c6cfd220438532b154d19be65fc0e424cfa767`.

## Checks actually run

- `python scripts/validate-boundary-first.py --check --path docs/design/skill/skill.md --path docs/design/system/system.md`: passed, structure and references only.
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/design/skill/skill.md`: passed with zero errors or warnings.
- `python scripts/validate-markdown-readability.py docs/design/skill/skill.md`: passed with 46 advisory warnings.
- Python local-link existence check: all 18 links passed.
- `git diff --check`: passed for tracked changes; explicit model/prose checks cover the untracked model.

Independent Design Review must reassess the refined exact subject and the existing package before approval can be claimed. Structural success does not establish complete semantic transfer.
