# Retained common contract correction

Owning change: [change.json](change.json). This author-owned correction implements the user's request to define surviving common rules precisely before retiring source definitions. It does not claim independent review or source retirement.

## Scope and result

[Skill](../../design/skill/skill.md#common-contract-details-retained-by-consolidation) now defines the retained rules, applicable populations and approved equivalents/supersessions in one table. It covers metadata fields and profile markers, routing descriptions, normalized coverage, role fields and the two-line summary limit, role-stage vocabulary, once-only fenced/table vocabulary presentation, enumerations, rule repetition/scope labeling, summary output and complete skeletons. The table expressly distinguishes retained specialist asset requirements from transferred common definitions.

The source dispositions for Readability R16–18 and R29–35 now point to precise transferred rules. Existing conditional-reference and asset amendments remain applicable; obsolete proposal metadata is not reinstated. An unknown equivalent or population prevents retirement of its source definition. No source, skill, validator, asset, System text or follow-up was changed by this correction.

## Basis and applicability

Prior Skill subject: `sha256:fc43e6c1159274721a41d8e56478c6b78ac55ea32e8fcc028293cd39a5e38171`.

Corrected Skill subject: `sha256:8e551e0ebcb35d7bd165baf5dcc833ff82a266c995eb1e25e80ebc2e0e2aceb2`.

The original [authoring evidence](design-authoring.md) remains a snapshot of the earlier subject and cannot establish validation of the corrected model. The independently approved proposal and unchanged System subjects retain their original meaning. This correction still requires independent Design Review; no Design judgment exists to renew.

Inspected source basis: Skill Contract R3, R11, R29–34; Skill Readability R11–28 and R32–35; Proposal simplification R2–7/35/39; Proposal Review simplification R18/20/22; Proposal-family assets PFA-R3/14/29–31; Simplified Proposal Contract SPC-R1–6. Existing metadata schema and readability validator were inspected as implementation consumers, not treated as authority for an exception. SKL-DEC-01–05 remain unchanged; their application now includes the precise retained table.

## Checks actually run

- `python scripts/validate-boundary-first.py --check --path docs/design/skill/skill.md --path docs/design/system/system.md`: passed, structure and references only.
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/design/skill/skill.md`: passed, zero errors or warnings.
- `python scripts/validate-markdown-readability.py docs/design/skill/skill.md`: passed with 46 advisory long-line warnings.
- Python local-link existence check: all 18 local Skill links passed.
- `git diff --check`: passed; this checks tracked diffs, while the untracked model is covered by the explicit model/prose checks above.

No executable behavior changed and no new tests were added. The remaining step is independent Design Review of the corrected exact subject and its declared package.
