# Vision Skill Explain Change

## Summary

This change adds the upstream `vision` skill and the supporting proposal, review, governance, README ownership, generated-output, and validation-routing changes needed to use it safely.

The implementation creates the method and distribution surfaces only. It deliberately does not create the initial root `vision.md` or insert generated README vision front-matter. Initial project vision authoring remains a later explicit `vision create` invocation.

## Problem

RigorLoop had workflow guidance, proposal/spec artifacts, architecture practices, and a public README, but it did not have one compact canonical project-vision artifact or a safe skill for creating and revising it.

That created three practical risks:

- users and contributors had to infer project identity from workflow details and README prose;
- proposals could change project direction without an explicit fit check;
- agents could treat vision text as ordinary README maintenance and overwrite authorial judgment or rewrite too broadly.

The accepted proposal chose a dedicated `vision` skill, `vision.md` as future canonical project-vision source, generated README front-matter bounded by markers, and `Vision fit` checks in proposal/proposal-review.

## Decision Trail

- Proposal: `docs/proposals/2026-04-29-vision-skill.md`
- Spec: `specs/vision-skill.md`
- Test spec: `specs/vision-skill.test.md`
- Plan: `docs/plans/2026-04-29-vision-skill.md`
- Change metadata: `docs/changes/2026-04-29-vision-skill/change.yaml`
- Architecture: not required. The approved spec changes skills, governance, README ownership, proposal guidance, generated skill/adapter output, and selector routing without introducing a new runtime boundary, service, data store, or architecture package.
- Code-review: clean with notes, no findings.
- Verify: branch-ready after correcting tracked handoff metadata and readiness wording.

Requirement and plan mapping:

| Requirement IDs | Implementation surface | Plan milestone |
| --- | --- | --- |
| `R1`-`R28`, `R56`-`R74` | `skills/vision/SKILL.md` | M1 |
| `R29`-`R42`, `R46`-`R55`, `R75`-`R78` | `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `README.md` | M2 |
| `R43`-`R45` | `.codex/skills/`, `dist/adapters/`, `dist/adapters/manifest.yaml` | M3 |
| `R79`-`R80` | `scripts/validation_selection.py`, `scripts/validate-readme.py`, `scripts/test-select-validation.py` | M5 |
| `AC1`-`AC12` | Milestones M1-M5 plus closeout validation | M4-M5, code-review, verify |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/vision/SKILL.md` | Added the canonical `vision` skill with create, revise, and mirror modes; source-of-truth rules; README marker rules; privacy, research, Markdown, output reporting, and bounded-read guidance | Provides a safe process for producing or updating project vision without making vision a normal lifecycle stage | `R1`-`R28`, `R40`-`R42`, `R56`-`R74`, proposal option 3 | `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `test ! -e vision.md` |
| `skills/proposal/SKILL.md` | Added required `Vision fit` guidance for new and substantively revised proposals, including exact behavior when no root `vision.md` exists | Makes proposal fit visible and prevents proposals from silently redefining project vision | `R29`-`R35`, `R75`-`R78` | `python scripts/test-skill-validator.py` |
| `skills/proposal-review/SKILL.md` | Added review rules for missing `Vision fit`, nonexistent-vision claims, conflict classification, and explicit exceptions | Gives reviewers a stable outcome path: revise proposal, revise vision, or record explicit exception | `R36`-`R39`, `R75`-`R78`, `AC4`, `AC12` | `python scripts/test-skill-validator.py` |
| `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md` | Documented `vision.md` as subordinate to `CONSTITUTION.md`, above generated README front-matter, and upstream of the per-change workflow | Keeps governance, agent instructions, and workflow routing consistent | `R40`-`R42`, `R46`-`R55`, `AC5`, `AC10` | skill validator governance regression and lifecycle validation |
| `README.md` | Added ownership wording for future marker-bounded README front-matter generated from `vision.md` | Public README needs to state the source boundary without inserting generated vision content in this slice | `R10`-`R13`, `R25`-`R26`, `R51`-`R55`, `AC8`, `AC10` | `python scripts/validate-readme.py README.md`, `python scripts/validate-readme.py README.md --vision-markers` |
| `.codex/skills/` | Refreshed generated Codex runtime skill mirrors through `scripts/build-skills.py` | Generated Codex output must match canonical skill sources and must not be hand-edited | `R43`, `AC6` | `python scripts/build-skills.py --check` |
| `dist/adapters/` and `dist/adapters/manifest.yaml` | Refreshed public Codex, Claude Code, and opencode adapter outputs through `scripts/build-adapters.py --version 0.1.1`; added portable `vision` skill files without adding an opencode command alias | Public adapter packages must distribute the new skill and updated proposal/proposal-review guidance from canonical sources | `R44`-`R45`, `AC7` | `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1` |
| `scripts/test-skill-validator.py` | Added focused content regressions for the vision skill, proposal `Vision fit`, proposal-review conflict handling, and governance/README source-of-truth wording | Contract text is the implementation surface, so tests assert the required guidance directly | `T1`-`T7`, `T12` | `python scripts/test-skill-validator.py` |
| `scripts/validation_selection.py` | Classified root `README.md` as `readme`, added selected checks for README validation and marker validation, and selected marker validation when a marker block is present or the vision skill is in scope | Verify found PR-mode CI blocked on `README.md` as `unclassified-path`; M5 made README an approved supported surface | `R79`-`R80`, `AC9` | `python scripts/select-validation.py --mode pr --base origin/main --head HEAD`, `python scripts/test-select-validation.py` |
| `scripts/validate-readme.py` | Added lightweight README validation plus optional standalone vision marker boundary validation | Gives selector-selected README checks a deterministic command without adding a README mirror helper | `R79`-`R80`, `AC9` | `python scripts/validate-readme.py README.md`, `python scripts/validate-readme.py README.md --vision-markers` |
| `scripts/test-select-validation.py` | Added selector regressions for README routing, marker-validation selection, PR-mode README classification, and malformed marker detection | Prevents approved README edits from becoming future PR-mode selector blockers | `T9`, `AC9` | `python scripts/test-select-validation.py` |
| `docs/proposals/2026-04-29-vision-skill.md`, `specs/vision-skill.md`, `specs/vision-skill.test.md`, `docs/plans/2026-04-29-vision-skill.md`, `docs/plan.md` | Added and maintained the proposal/spec/test/plan artifacts and corrected stale readiness text during verify | Keeps the lifecycle record aligned with the actual implementation and handoff state | workflow contract, plan M1-M5, verify findings | artifact lifecycle validation |
| `docs/changes/2026-04-29-vision-skill/change.yaml` and this file | Recorded the changed surfaces, validation evidence, clean review, verify result, and durable rationale | Keeps non-trivial change evidence out of chat-only state | workflow contract and explain-change skill | change metadata validation and lifecycle validation |

## Tests Added Or Changed

- `scripts/test-skill-validator.py` now asserts the `vision` skill mode contract, README marker rules, privacy/research boundaries, bounded-read guidance, proposal `Vision fit`, proposal-review conflict handling, and governance/README source-of-truth wording.
- `scripts/test-select-validation.py` now asserts `README.md` selects `readme.validate`, vision marker validation is selected when marker state or vision scope requires it, PR-mode README changes no longer block as `unclassified-path`, and malformed standalone marker blocks fail validation.
- `scripts/validate-readme.py` is a new lightweight validation command used by selector-selected checks. It verifies README readability and optional standalone marker-pair structure; it is not a README mirror helper.
- `specs/vision-skill.test.md` maps `R1`-`R80` and `AC1`-`AC12` to contract checks, generated-output checks, selector checks, lifecycle checks, manual README proof, and broad smoke.

The test level is appropriate because the implementation is primarily skill/guidance text plus selector routing. The highest-risk executable behavior is selector/README validation, so that area has focused regression tests.

## Verification Evidence

Verify passed after correcting stale tracked metadata and readiness wording.

Commands run successfully after final verify readiness correction:

- `python scripts/select-validation.py --mode pr --base origin/main --head HEAD`
- `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-29-vision-skill/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-29-vision-skill.md --path docs/proposals/2026-04-29-vision-skill.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-29-vision-skill/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-vision-skill`
- `test ! -e vision.md`
- `git diff --check origin/main..HEAD -- .`

The PR-mode selector selected these stable check IDs:

- `skills.validate`
- `skills.regression`
- `skills.drift`
- `adapters.regression`
- `adapters.drift`
- `adapters.validate`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`
- `readme.validate`
- `readme.vision_markers`
- `selector.regression`
- `broad_smoke.repo`

PR-mode CI passed the selected checks. Broad smoke also passed. The broad-smoke lifecycle pass emitted unrelated legacy warnings for older proposal files, but exited successfully and did not block this change.

Manual proof:

- `test ! -e vision.md` confirms the initial project vision was not created by this implementation.
- README marker validation confirms no standalone generated vision marker block is present.
- The implementation did not add a README mirror helper script.

Hosted CI has not been observed in this stage; PR-stage review owns PR body/open readiness and hosted CI observation.

## Review Resolution Summary

Code-review completed clean with notes and no findings. There were no material findings, no `review-resolution.md` was required, and `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-vision-skill` passed with zero reviews, findings, log entries, and resolution entries.

Verify did identify lifecycle drift:

- tracked plan/change metadata still pointed to `code-review`;
- spec and test-spec Readiness sections still pointed to earlier handoff stages.

Those verify findings were resolved by tracked metadata/readiness updates before this explanation was written.

## Alternatives Rejected

- Keep README as the only project-positioning surface: rejected because proposal fit and project identity would keep drifting across README prose and workflow details.
- Add `vision.md` without a skill: rejected because future agents would still lack safe create/revise/mirror behavior and overwrite protection.
- Add `vision` as a normal workflow stage: rejected because the accepted model keeps vision upstream and dormant by default, not inside every per-change chain.
- Create the initial `vision.md` in this implementation: rejected because project vision is authorial judgment and requires a separate explicit `vision create` invocation.
- Add a README mirror helper script now: rejected because marker behavior is contract-level guidance in v1; automation is deferred until repeated mirror drift proves it is needed.
- Rewrite legacy proposals to add `Vision fit`: rejected because the spec preserves legacy proposals unless they are substantively revised after adoption.
- Add an opencode command alias for `vision`: not done because existing opencode aliases remain limited to the curated lifecycle command set while the full skill is distributed under opencode skills.

## Scope Control

- No root `vision.md` was created.
- No generated README vision front-matter was inserted.
- No README mirror helper script was added.
- `vision` was not added to the normal lifecycle chain.
- No existing proposals were rewritten solely to add `Vision fit`.
- No generated `.codex/skills/` or `dist/adapters/` output was hand-edited; generated surfaces were refreshed through existing generators.
- No architecture package or ADR was added because this change did not introduce a new architecture boundary.

## Risks And Follow-Ups

- The next substantive step is a separate `vision create` invocation to author the initial root `vision.md` and README front-matter. That artifact needs human review before it becomes current.
- Vision prose quality remains review-based in this slice. No validator enforces whether a generated vision is good project judgment.
- Hosted CI is still a PR-stage observation.
- Future README mirror drift may justify a helper script, but that is intentionally deferred.

## PR Handoff Summary

- The branch is `branch-ready` from verify evidence.
- `explain-change` is complete and recorded in this file.
- PR #23 opened, hosted CI passed, and the PR merged into `main` at `992d380a6c085bcf612cc627a2c038c0d1a1ff25`.
- Post-merge cleanup moved the plan to `Done`.

## Readiness

- `implement`, `code-review`, `verify`, and `explain-change` are complete for this change.
- PR #23 is merged.
- No repository workflow stage remains pending for this implementation.
