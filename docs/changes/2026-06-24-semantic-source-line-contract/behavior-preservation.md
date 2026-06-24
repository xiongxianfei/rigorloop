# Behavior Preservation: Semantic Source-Line Contract

## Scope

This proof records behavior preservation for the first-slice documentation source-line contract.
It covers M1 validator behavior, M2 Tier A cleanup and formatter guardrails, and M3 selected-validation routing.

The first slice changes source review and validation routing.
It does not change Markdown rendering, workflow stage order, generated-content ownership, skill behavior, historical documentation, or public runtime behavior.

## Preservation Matrix

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Rendered README | Current README content rendered from Markdown, with vision marker content generated from `VISION.md` | M2 edited only source-line shape in human-authored README prose outside the marker block; `python scripts/validate-readme.py` passed | preserved |
| README marker ownership | `<!-- vision:start -->` through `<!-- vision:end -->` is generated from `VISION.md` | M2 left the README marker block bounded and validated it with `python scripts/validate-readme.py README.md --vision-markers`; canonical wording cleanup occurred in `VISION.md` | preserved |
| VISION meaning | Existing project vision states the traceable lifecycle and reviewable software-engineering artifact positioning | M2 joined the source line for the existing sentence without changing wording or rendered meaning | preserved |
| Retired vocabulary checks | Existing README and guide validation remain responsible for vocabulary and guide-system checks | `python scripts/validate-readme.py` and `python scripts/validate-guide-system.py` passed after M2; M3 does not replace those checks | preserved |
| Skill behavior | Existing canonical skill validation and skill regressions own skill contract behavior | M3 routes `skills/**/SKILL.md` to documentation prose audit in addition to existing skill checks; it does not change skill files or skill execution behavior | preserved |
| Historical documentation | Specs, plans, review records, learn artifacts, historical evidence, and third-party documentation remain outside first-slice prose enforcement | M3 selector tests prove Tier C paths do not select `documentation_prose.enforce` or `documentation_prose.audit` for first-slice prose validation | preserved |
| Source reviewability | Repeated hard-wrap corrections showed source lines could obscure semantic units | M1 fixtures and M2 Tier A cleanup make deterministic source-line defects fail; M3 selected validation routes Tier A to enforcement and Tier B to audit | strengthened |

## Routing Preservation

| Changed path class | Selected prose behavior | Existing checks preserved |
| --- | --- | --- |
| `README.md` | `documentation_prose.enforce` | `readme.validate`, `readme.vision_markers`, `guide_system.validate` |
| `VISION.md` | `documentation_prose.enforce` | `readme.vision_markers`, `guide_system.validate` |
| `skills/**/SKILL.md` | `documentation_prose.audit` | `skills.validate`, `skills.regression`, `skills.generation_regression`, `skills.drift`, adapter drift checks where already selected |
| `docs/changes/**/explain-change.md` | `documentation_prose.audit` | change-local lifecycle and registered-evidence checks |
| Tier C Markdown | no first-slice prose validation route | existing lifecycle, review-artifact, learn, guide-system, or release checks remain responsible according to existing category |

## Validation Evidence

- `python scripts/test-select-validation.py` passed with selected-validation routing coverage.
- `python scripts/test-documentation-prose-validator.py` passed with validator behavior and fixture coverage.
- `python scripts/select-validation.py --mode explicit --path README.md --path VISION.md` selects Tier A prose enforcement plus existing README marker and guide checks.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-semantic-source-line-contract/` validates formal review recording.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-semantic-source-line-contract/change.yaml` validates change metadata.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/documentation-source-formatting.md --path docs/plans/2026-06-24-semantic-source-line-contract.md --path docs/plan.md --path docs/changes/2026-06-24-semantic-source-line-contract/change.yaml --path docs/changes/2026-06-24-semantic-source-line-contract/behavior-preservation.md` validates lifecycle-managed artifacts and this proof.

## Result

The first slice preserves rendered documentation meaning, README marker ownership, existing README and guide checks, skill behavior, and historical documentation boundaries.
It strengthens source reviewability by adding selector routing for the already-approved prose validator without expanding enforcement beyond Tier A.
