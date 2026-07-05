# Markdown Readability Contract Explain Change

## Summary

This change makes generated and generator-shaped Markdown easier to review in source and rendered form.
It adds a dedicated Markdown readability validator, fixture-backed checks, selector integration for README and `VISION.md`, canonical generated-region marker validation, and selected skill and skeleton guidance for generated artifacts.

The implementation intentionally avoids fixed-width prose wrapping, manual-proof contract enforcement, mandatory diagrams, historical Markdown reflow, and hand-edited generated public adapter bodies.

## Problem

RigorLoop artifacts are reviewed as source diffs and rendered Markdown.
Previous generated prose could render acceptably while splitting meaningful phrases such as `AI agents`, `proposal to spec`, and `reviewable in Git` across physical source lines.
The project also needed stable generated artifact guidance so repeated documents remain skim-first, traceable, and generated from canonical sources.

## Decision Trail

| Source | Decision or requirement | Implementation link |
| --- | --- | --- |
| Proposal | Use a readability contract instead of a fixed Markdown line-length rule. | `scripts/validate-markdown-readability.py` reports generic long lines as audit-only and does not fail solely on line width. |
| Proposal | Make `scripts/validate-markdown-readability.py` the owner validator. | Added the owner validator and composed it through selector routing instead of duplicating policy in downstream validators. |
| Spec R1-R10 | Preserve semantic source lines and structured Markdown surfaces. | Added deterministic hard-wrap checks, block exclusions, audit-only warnings, and generated artifact guidance. |
| Spec R20 | Do not introduce manual-proof contracts. | Skill guidance explicitly says readability guidance alone must not require manual-proof contracts. |
| Spec R21-R27 | Use canonical generated-region markers and source ownership. | Added generated-region marker parsing, pairing validation, and metadata checks. |
| Spec R32-R35 | Enforce README and `VISION.md` changed sections without historical migration. | Selector-composed readability commands carry changed-section ranges; historical full-file concerns were closed by direct current-state validation. |
| Spec R45-R48 | Encourage diagrams only when useful; never require them. | Selected skills state that diagrams are optional and must reduce cognitive load. |
| Spec R49-R50 | Validate generated adapter output from canonical sources and do not hand-edit generated bodies. | `build-skills --check`, `test-build-skills.py`, and `test-adapter-distribution.py` passed after M2. |
| Plan M1 | Add the validator and deterministic fixtures. | Implemented M1 and closed it after code-review M1 R3. |
| Plan M2 | Align selected generated artifact guidance and proof. | Implemented M2 and closed it after code-review M2 R1. |

Architecture was not required; `spec-review-r1` recorded no new runtime, persistence, deployment, external integration, or hard-to-reverse architecture decision.

## Diff Rationale By Area

| Area | Files | Change | Reason | Evidence |
| --- | --- | --- | --- | --- |
| Readability validator | `scripts/validate-markdown-readability.py`, `scripts/test-markdown-readability-validator.py` | Added `MDREAD-*` checks for semantic hard-wrap fixtures, generated-region markers, placeholders, block exclusions, and audit-only warnings. | Own deterministic readability policy in one script. | `python scripts/test-markdown-readability-validator.py`; `python scripts/validate-markdown-readability.py`. |
| Selector integration | `scripts/validation_selection.py`, `scripts/test-select-validation.py` | Added selected readability commands with changed-section ranges for README and `VISION.md`. | Preserve changed-section enforcement when existing validators compose the owner validator. | `python scripts/test-select-validation.py`; focused selector regression. |
| Generated artifact guidance | selected `skills/*/SKILL.md` files | Added `Generated Markdown readability` guidance for semantic lines, stable IDs, tables, commands, optional diagrams, and manual-proof exclusion. | Make repeated generated artifacts predictable without making skeletons policy owners. | `python scripts/test-skill-validator.py MarkdownReadabilityGuidanceTests`; `python scripts/validate-skills.py`. |
| Skeleton declarations | selected skeleton assets under `skills/*/assets/` | Added top-level readability metadata comments. | Keep output-shape expectations discoverable near the template. | `MarkdownReadabilityGuidanceTests`; `python scripts/build-skills.py --check`. |
| Generated-output proof | canonical skill sources and adapter validation | Validated generated skill and adapter output from canonical sources. | Prove generated public adapter bodies were not hand-edited. | `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`. |
| Lifecycle evidence | `docs/changes/2026-07-04-markdown-readability-contract/`, `docs/plans/2026-07-04-markdown-readability-contract.md`, `docs/plan.md` | Recorded proposal/spec/test/plan/review evidence, behavior preservation, review closeout, and current handoff state. | Keep workflow state reviewable and resumable. | Review-artifact, change-metadata, lifecycle, and whitespace validation. |

## Tests Added Or Changed

| Test or command | Proves | Why this level |
| --- | --- | --- |
| `scripts/test-markdown-readability-validator.py` | Validator behavior for hard-wrap regressions, block exclusions, generated-region markers, placeholders, and audit-only warnings. | Unit and fixture tests directly exercise deterministic check behavior. |
| `scripts/test-select-validation.py` | Selector-composed readability commands include changed-section ranges and fail changed README hard-wrap fixtures. | Integration test covers validator composition and command rendering. |
| `scripts/test-skill-validator.py MarkdownReadabilityGuidanceTests` | Selected skills and skeletons carry generated Markdown readability guidance. | Focused regression checks the M2 generated-artifact contract. |
| `scripts/test-build-skills.py` | Generated skill build behavior remains valid. | Generated-output test proves canonical skill source compatibility. |
| `scripts/test-adapter-distribution.py` | Adapter distribution remains valid and generated bodies are not hand-edited. | Smoke/integration coverage matches the generated adapter boundary. |

## Validation Evidence Available Before Final Verify

| Command | Result |
| --- | --- |
| `python scripts/test-markdown-readability-validator.py` | passed |
| `python scripts/validate-markdown-readability.py --help` | passed |
| `python scripts/validate-markdown-readability.py` | passed with audit-only warnings `MDREAD-002=63`, `MDREAD-003=5` |
| `python scripts/test-select-validation.py` | passed with 125 tests after M1 review-resolution |
| `python scripts/validate-markdown-readability.py README.md VISION.md --verbose` | passed with audit-only warnings only |
| `python scripts/test-skill-validator.py MarkdownReadabilityGuidanceTests` | passed |
| `python scripts/validate-skills.py` | passed |
| `python scripts/build-skills.py --check` | passed |
| `python scripts/test-build-skills.py` | passed |
| `python scripts/test-adapter-distribution.py` | passed with 130 tests |
| `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract` | passed before explain-change |
| `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | passed before explain-change |
| `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` | passed before explain-change |
| `git diff --check -- ...` | passed before explain-change |

Hosted CI has not been observed in this stage.
Final `verify` and PR readiness are not claimed by this explanation.

## Review Resolution Summary

Material finding count: 4.

| Disposition | Count | Finding IDs |
| --- | --- | --- |
| accepted | 3 | `MDREAD-PR1`, `MDREAD-PR2`, `MDREAD-M1-CR1` |
| rejected | 1 | `MDREAD-M1-CR2` |
| open | 0 | none |

Review-resolution details are recorded in `docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md`.
Code-review M1 R3 and code-review M2 R1 completed clean-with-notes with no material findings.

## Alternatives Rejected

| Alternative | Reason rejected |
| --- | --- |
| Fixed-width Markdown wrapping | It recreates the source-review failure mode this change is meant to prevent. |
| Auto-format all Markdown prose | It can split meaning-bearing prose and create noisy historical churn. |
| Put readability policy into guide or skill validators | It would duplicate policy and let validator behavior drift. |
| Require diagrams everywhere | The spec requires diagrams to be useful, not mandatory. |
| Introduce manual-proof contracts in this slice | Spec R20 excludes them from this change. |
| Hand-edit generated public adapter bodies | Spec R50 prohibits this; generated-output proof uses canonical sources. |

## Scope Control

This change does not mass-reflow historical Markdown.
It does not impose a universal line-length limit.
It does not make subjective prose quality fail validation.
It does not change runtime product behavior.
It does not add architecture, persistence, deployment, or external integration surfaces.

## Risks And Follow-Ups

The repeated generated Markdown guidance in selected skills could become a maintenance point if many more skills adopt the same text.
This is acceptable for the current slice because the plan scoped M2 to selected high-value surfaces and generated-output validation passed.

Final `verify` still needs to rerun the required branch-readiness checks and confirm artifact-code-test coherence before PR handoff.
