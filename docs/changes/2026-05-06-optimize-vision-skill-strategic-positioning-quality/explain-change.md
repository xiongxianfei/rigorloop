# Explain Change

## Summary

This change optimizes the `vision` skill so it identifies strategic project positioning before drafting or materially repositioning `VISION.md`. It also retires active lowercase `vision.md` migration behavior from user-facing guidance and repository validation.

The branch re-centers RigorLoop from a lower-level "Git-first starter kit" framing to a rigorous software engineering workflow for AI coding agents. Git, CI, pull requests, and repository-local artifacts remain compatibility surfaces, but they are no longer the project category.

## Problem

The existing `vision` skill had strong editing and README synchronization mechanics, but it did not force a strategic positioning pass before writing. That let a compatibility surface become the headline when the higher-level category was a methodology/workflow. The same change also needed to retire old lowercase `vision.md` migration handling across active guidance and validation, now that root `VISION.md` is canonical.

## Decision Trail

| Source | Decision | Effect on diff |
| --- | --- | --- |
| Proposal | Adopt a strategic-positioning layer instead of replacing the skill or only adding examples. | Updated the existing `vision` skill and tests instead of creating a new skill or prompt-output harness. |
| Proposal | Store durable positioning rationale in `docs/vision/strategic-positioning.md`. | Added the rationale artifact and linked it from this explanation. |
| Proposal | Use static assertions for this slice. | Added and tightened `scripts/test-skill-validator.py` assertions rather than building a model-output scoring harness. |
| Spec | `R1`-`R8`, `R63`-`R67`: root `VISION.md` is canonical and active lowercase `vision.md` behavior is retired. | Updated governance/README/proposal guidance, selector routing, selector tests, and skill assertions. |
| Spec | `R20`-`R31`: state-based establishment, update, sync, and retired lowercase path boundaries. | Updated `skills/vision/SKILL.md`; later fixed `CR1-F1` so retired lowercase `vision.md` cannot block explicit `VISION.md` creation. |
| Spec | `R32`-`R39`, `R73`-`R86`: word limits, strategic-positioning pass, anti-anchor rule, methodology-as-product, rationale artifact, and final quality gates. | Updated `skills/vision/SKILL.md`, `VISION.md`, `README.md`, rationale artifact, and static assertions. |
| Spec | `R40`-`R48`: README front-matter remains marker-bounded and derived from `VISION.md`. | Preserved README markers and validated marker boundaries after README changes. |
| Spec | `R49`-`R62`: proposal and proposal-review `Vision fit` use canonical `VISION.md`. | Updated `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` plus generated outputs. |
| Plan | M1: proof map, static assertions, selector behavior. | Updated `specs/vision-skill.test.md`, selector tests, and `scripts/validation_selection.py`. |
| Plan | M2: canonical skill guidance and rationale artifacts. | Updated authored skills, `CONSTITUTION.md`, `VISION.md`, README front-matter/body, and `docs/vision/strategic-positioning.md`. |
| Plan | M3: generated output refresh. | Regenerated `.codex/skills/` and `dist/adapters/` through repository generators. |
| Plan | M4 and downstream review/verify. | Closed lifecycle/review evidence, fixed review and verify findings, and moved readiness to PR handoff. |

No architecture package or ADR was required. The plan records that this change stays in workflow-governance guidance, tests, validation, generated text, and rationale artifacts without adding runtime data flow, persistence, network integration, schemas, deployment behavior, or release packaging.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `CONSTITUTION.md` | Reframed project purpose around rigorous AI-agent engineering workflow and made Git/CI/PRs compatibility surfaces. | Align governance with the accepted strategic center. | Proposal goals; spec `R1`-`R8`, `R80`-`R86`. | Selected CI `artifact_lifecycle.validate`; final verify. |
| `VISION.md` | Repositioned the project vision around trustworthy AI-assisted change delivery and durable evidence. | Apply the methodology/workflow category rather than substrate-centered framing. | Spec `R32`-`R39`, `R73`-`R86`. | Word count 383; final verify; README marker validation. |
| `README.md` | Regenerated front-matter from `VISION.md` and fixed active body text that still said "Git-first starter kit". | Keep README aligned with canonical vision while preserving repository-local compatibility messaging. | Spec `R5`-`R6`, `R40`-`R48`; verify drift finding. | `validate-readme.py`, `validate-readme.py --vision-markers`, no-match scan for stale Git-first framing. |
| `docs/vision/strategic-positioning.md` | Added compact positioning rationale and authority wording. | Preserve durable rationale for the material vision repositioning without making it authoritative over `VISION.md`. | Proposal recommended placement; spec `R73`-`R79`. | `artifact_lifecycle.validate`; test spec `T4`, `T10`, `T11`. |
| `specs/vision-skill.md` | Added the strategic-positioning contract, 750/900-word limits, rationale artifact rules, anti-anchor rule, methodology-as-product guidance, and lowercase retirement requirements. | Turn accepted proposal decisions into the governed feature contract. | Proposal decision log; spec-review records. | `spec-review-r3` approved; lifecycle validation. |
| `specs/vision-skill.test.md` | Added traceable proof map for the new requirements and edge cases. | Make the implementation test-driven and reviewable. | Spec requirements and plan M1. | `artifact_lifecycle.validate`; selected CI. |
| `skills/vision/SKILL.md` | Added strategic-positioning workflow, word-budget policy, rationale artifact behavior, anti-anchor guidance, final quality gates, and state-based lowercase retirement. | Implement the approved behavior in the canonical skill. | Spec `R9`-`R39`, `R68`-`R86`. | `validate-skills.py`, `test-skill-validator.py`. |
| `skills/proposal/SKILL.md` | Anchored `Vision fit` to root `VISION.md` and removed lowercase no-vision exceptions. | Keep proposals aligned with the canonical vision model. | Spec `R49`-`R57`. | `test-skill-validator.py`; selected CI. |
| `skills/proposal-review/SKILL.md` | Updated proposal-review checks for `Vision fit`, canonical `VISION.md`, and explicit exceptions. | Keep review behavior aligned with proposal guidance. | Spec `R58`-`R62`. | `test-skill-validator.py`; selected CI. |
| `scripts/validation_selection.py` | Stopped classifying root `vision.md` as a supported root vision path and routed `docs/vision/*.md` through lifecycle validation. | Retire lowercase validation behavior and validate durable rationale artifacts. | Spec `R63`-`R67`; plan M1. | `test-select-validation.py`; selector probes. |
| `scripts/test-select-validation.py` | Added/updated selector regressions for canonical `VISION.md`, retired root `vision.md`, and rationale path routing. | Prove selector behavior changed intentionally. | Test spec `T8`, `T12`. | `python scripts/test-select-validation.py`. |
| `scripts/test-skill-validator.py` | Added static assertions for strategic positioning, word policy, generated rationale, proposal fit, and `CR1-F1` regression. | Enforce the accepted static-assertion strategy and prevent stale wording from returning. | Test spec `T1`-`T12`; code-review `CR1-F1`. | `python scripts/test-skill-validator.py`. |
| `.codex/skills/` | Regenerated local Codex skill mirrors. | Keep generated runtime output derived from canonical `skills/`. | Spec `R64`; plan M3. | `build-skills.py --check`. |
| `dist/adapters/` | Regenerated public adapter skill copies for Codex, Claude Code, and opencode. | Keep adapter packages in sync with canonical skill changes. | Spec `R65`; plan M3. | `test-adapter-distribution.py`, `build-adapters.py --check`, `validate-adapters.py`. |
| `docs/proposals/...`, `docs/plans/...`, `docs/plan.md` | Added/updated lifecycle artifacts and readiness state. | Preserve proposal, plan, validation, review, verify, and next-stage evidence. | Constitution lifecycle rules; plan M4. | `artifact_lifecycle.validate`, change metadata validation. |
| `docs/changes/.../review-*` and `reviews/*` | Recorded material findings, dispositions, closeout evidence, and clean reruns. | Preserve formal review history and satisfy review-resolution contract. | Review rules; code-review/spec-review/proposal-review records. | `validate-review-artifacts.py --mode closeout`. |
| `docs/learn/sessions/...` | Recorded a lesson about isolated review material finding records. | Capture recurring workflow learning surfaced during this change. | Explicit learn request and workflow learning rules. | Selected CI lifecycle checks. |

## Tests Added Or Changed

| Test ID | Proof surface | What it proves | Why this level is appropriate |
| --- | --- | --- | --- |
| `T1` | `scripts/test-skill-validator.py` plus manual diff review | Active guidance uses canonical `VISION.md` and keeps historical lowercase references archival. | Contract text and guidance are the implementation surface. |
| `T2` | `scripts/test-skill-validator.py` | The vision skill remains state-based and bounded, including explicit establishment and retired lowercase path rules. | Static assertions catch drift in the skill instructions. |
| `T3` | `scripts/test-skill-validator.py`, word count | Word policy, publication safety, and no requirements-like vision prose are present. | The change is guidance/prose, not runtime behavior. |
| `T4` | `scripts/test-skill-validator.py`, rationale artifact inspection | Strategic-positioning rationale is created, supporting, and linked from change-local explanation. | Durable Markdown artifacts are the contract surface. |
| `T5` | `scripts/test-skill-validator.py` | Methodology, ordinary substrate, and true substrate examples are encoded. | Static fixtures directly target the original positioning failure. |
| `T6` | `scripts/test-skill-validator.py`, README validators | README marker boundaries and derived front-matter are preserved. | README marker validation is already repo-owned. |
| `T7` | `scripts/test-skill-validator.py` | Proposal/proposal-review `Vision fit` uses canonical `VISION.md`. | Proposal behavior is skill-guidance text. |
| `T8` | `scripts/test-select-validation.py`, selector probes | Root `VISION.md` is supported; root `vision.md` is blocked/unclassified as retired. | Selector routing is script behavior and needs executable regression tests. |
| `T9` | `validate-skills.py`, `build-skills.py --check` | Canonical and generated skills remain valid and in sync. | Generated-output drift must be proven by generators. |
| `T10` | Artifact lifecycle validation and rationale inspection | Current material repositioning has durable rationale and explanation. | Manual/artifact validation is appropriate for rationale quality. |
| `T11` | Review/change metadata validators | Review and change-local evidence are structurally complete. | The workflow contract is artifact-based. |
| `T12` | Selected CI over changed paths | The selector chooses the expected repo-owned checks for this change. | End-to-end selected CI proves check routing and execution. |

## Verification Evidence

Final verification passed on 2026-05-07.

Commands run and passed:

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `python scripts/validate-readme.py README.md`
- `python scripts/validate-readme.py README.md --vision-markers`
- `git diff --check -- .`
- trailing-whitespace scan over changed files
- `bash scripts/ci.sh --mode explicit $( (git diff --name-only origin/main..HEAD; git diff --name-only; git ls-files --others --exclude-standard) | sort -u | sed 's/^/--path /' )`

Selected CI passed these check IDs:

- `skills.validate`
- `skills.regression`
- `skills.drift`
- `adapters.regression`
- `adapters.drift`
- `adapters.validate`
- `review_artifacts.validate`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`
- `readme.validate`
- `readme.vision_markers`
- `selector.regression`

Additional manual checks:

- `VISION.md` word count: 383 words, below the 750-word normal cap and 900-word maximum.
- `rg` no-match scan confirmed active vision surfaces no longer contain `Git-first`/`git-first` after the verify-found README drift fix.
- Selector output over the full branch diff reported `broad_smoke_required: false`.

Hosted CI was not observed. Broad smoke was not required by the active plan or selector output.

Artifact lifecycle validation emitted the known reviewer-attention warning for older lifecycle-transition wording in a Done entry in `docs/plan.md`. That warning is unrelated baseline text from completed historical plans, not stale lifecycle state for this active plan.

## Review Resolution Summary

Review resolution is closed in [review-resolution.md](review-resolution.md). There are 4 material findings total, all accepted and closed:

- `PR-1`: broadened lowercase `vision.md` retirement across active user-facing guidance and repo validation.
- `SR1-F1`: made 900 words the maximum allowed `VISION.md` length.
- `SR2-F1`: removed the alternate-cap exception from boundary behavior.
- `CR1-F1`: fixed explicit initial `VISION.md` creation so retired lowercase `vision.md` cannot block it.

Same-stage clean reruns:

- `proposal-review-r2`
- `spec-review-r3`
- `code-review-r2`
- `code-review-r3`

`review-log.md` lists no open findings, and review artifact closeout validation passes.

## Alternatives Rejected

- Keep the `vision` skill unchanged: rejected because it left the original substrate-anchoring failure mode intact.
- Add examples only: rejected because examples do not force the strategic category, audience, mechanism, tradeoff, and falsifiability pass.
- Replace the whole skill: rejected because existing edit authorization, README marker safety, security boundaries, and output reporting were useful.
- Add a prompt-output scoring harness now: rejected as too heavy for this slice; static assertions cover the durable contract.
- Store positioning rationale inside `VISION.md`: rejected because it would make the public vision into a worksheet.
- Rely only on final assistant output for rationale: rejected because RigorLoop expects durable, reviewable artifacts.
- Keep lowercase `vision.md` migration behavior as active behavior: rejected because migration is complete and active support weakens the canonical `VISION.md` model.

## Scope Control

Preserved non-goals:

- Did not turn `VISION.md` into a proposal, spec, architecture document, roadmap, feature list, or task tracker.
- Did not make `docs/vision/strategic-positioning.md` independently authoritative.
- Did not make `vision` a normal lifecycle stage.
- Did not require external research for ordinary vision drafting.
- Did not add runtime data flow, schemas, deployment behavior, release packaging, or adapter runtime execution.
- Did not hand-edit generated `.codex/skills/` or `dist/adapters/`; they were regenerated.
- Did not rewrite historical records solely to replace archival lowercase `vision.md` references.

## Risks And Follow-Ups

Remaining risks:

- Static assertions verify durable guidance phrases, not live prompt-output quality. That is intentional for this slice.
- Future editorial README or vision updates could reintroduce substrate-centered language. The active skill guidance and tests now make that easier to catch.

No required follow-up is open from this stage.

## PR Handoff Summary

- Branch contains accepted proposal, approved spec, active test spec, completed implementation milestones, closed review-resolution, clean code-review reruns, passed verify, refreshed explain-change, and synchronized Done lifecycle closeout.
- PR handoff is the final planned lifecycle step for this branch; merge is not used as a deferred plan-closeout trigger.
- Ready for PR review.
