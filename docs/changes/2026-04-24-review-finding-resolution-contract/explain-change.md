# Review finding resolution contract change explanation

## Summary

This change adds the review finding resolution contract for RigorLoop. It makes material review findings actionable, records durable review history, validates review-log and review-resolution structure, blocks downstream closeout on unresolved findings, and keeps canonical workflow skills plus generated adapter outputs aligned.

The implementation preserves lightweight clean reviews. The full `reviews/`, `review-log.md`, and `review-resolution.md` chain is required only when material findings exist or when a change independently creates detailed review records.

## Problem

Before this change, review feedback could be incomplete or scattered. A finding could point at a concern without evidence, required outcome, or safe resolution path; final dispositions had only the older accepted/rejected/deferred vocabulary; and downstream stages had no repository-owned structural check for unresolved material findings.

That made it possible for `verify`, `explain-change`, or `pr` to proceed while review feedback was still ambiguous, missing from durable artifacts, or only summarized in PR text.

## Decision Trail

The accepted proposal selected a durable review chain:

- first-pass material review findings are recorded before fixes;
- each finding includes evidence, required outcome, and safe resolution or `needs-decision` rationale;
- `review-log.md` indexes detailed review events;
- `review-resolution.md` records final dispositions, actions, rationale, owners, validation targets, and validation evidence;
- `verify`, `explain-change`, and `pr` block on unresolved closeout.

The approved spec is `specs/review-finding-resolution-contract.md`. It defines requirements `R1`-`R14a`, including complete findings, Review ID and Finding ID structure, `partially-accepted`, `needs-decision`, `Closeout status: open/closed`, closeout-gated validation, concise explanation/PR summaries, and generated adapter sync.

The approved architecture is `docs/architecture/2026-04-24-review-finding-resolution-contract.md`. It keeps per-change review parsing in a dedicated validator module instead of merging it into `change.yaml` metadata or top-level artifact lifecycle validation.

The execution plan split the work into four milestones:

- M1 added structure-mode review artifact parsing and validation.
- M2 added closeout-mode validation and CI changed-root integration.
- M3 aligned workflow guidance, canonical skills, `.codex/skills/`, and public adapter outputs.
- M4 closed lifecycle state, added this explanation, and ran final validation.

## Diff Rationale By Area

| Area | Files | Change | Reason | Source / Evidence |
| --- | --- | --- | --- | --- |
| Review artifact validation | `scripts/review_artifact_validation.py`, `scripts/validate-review-artifacts.py` | Added parsers and validators for detailed review files, canonical `review-log.md` entries, material Finding IDs, `review-resolution.md`, disposition values, closeout status, and blocking review closeout. | Satisfies `R2`-`R8h`, `R11`-`R11b`, and clean-review edge cases. | `T2`-`T9`, `T13`, `T15`; `python scripts/test-review-artifact-validator.py`. |
| Review artifact fixtures | `tests/fixtures/review-artifacts/` | Added valid and invalid review roots for structure and closeout mode. | Proves exact-one Review IDs, duplicate IDs, canonical log blocks, missing resolution entries, unsupported dispositions, and closeout blockers. | `T2`-`T9`, `T13`. |
| CI integration | `scripts/ci.sh` | Runs review-artifact structure validation for changed `docs/changes/<change-id>/` roots. | Enforces current changes without forcing historical artifact migration. | `T13`; `bash scripts/ci.sh`. |
| Workflow contract and docs | `specs/rigorloop-workflow.md`, `docs/workflows.md`, `CONSTITUTION.md`, `AGENTS.md` | Added expanded disposition vocabulary, complete-finding rules, closeout status rules, first-pass timing, and concise summary guidance. | Keeps repository guidance from contradicting the approved review-resolution contract. | `R14`-`R14a`; contract text checks in `scripts/test-review-artifact-validator.py`. |
| Canonical skills | `skills/*-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/explain-change/SKILL.md`, `skills/pr/SKILL.md`, `skills/workflow/SKILL.md` | Updated review-stage, closeout, explanation, PR, and orchestration guidance. | Ensures stage behavior records complete findings, blocks unresolved review-resolution state, and summarizes instead of duplicating detailed findings. | `R1`-`R10c`, `R14a`; skill validation and contract text checks. |
| Generated skill outputs | `.codex/skills/`, `dist/adapters/*` | Regenerated derived local Codex and public adapter skill packages. | Canonical skill changes must ship through generated Codex, Claude Code, and OpenCode outputs without drift. | `R12`-`R12c`; build and adapter validation. |
| Change-local artifacts | `docs/changes/2026-04-24-review-finding-resolution-contract/` | Added review records, review log, review resolution, metadata, and this explanation. | Gives reviewers durable evidence for findings, decisions, validation, and final rationale. | Closeout validation and change metadata validation. |
| Plan lifecycle | `docs/plans/2026-04-25-review-finding-resolution-contract.md`, `docs/plan.md` | Recorded milestone progress, validation, review fixes, and final done state. | Prevents stale lifecycle state before PR handoff. | Artifact lifecycle validation and CI. |

## Tests Added Or Changed

The primary test surface is `scripts/test-review-artifact-validator.py`.

| Test IDs | What The Tests Prove |
| --- | --- |
| `T1`, `T11` | Review guidance requires complete material findings and first-pass timing. |
| `T2`-`T5`, `T13` | Detailed review files, Review IDs, Finding IDs, canonical review-log blocks, and review-resolution links are structurally valid. |
| `T6`-`T8` | Disposition vocabulary, closeout status, `needs-decision`, `partially-accepted`, blocking review outcomes, and clean-review lightweight paths behave correctly. |
| `T9`, `T15` | Validator failures are actionable and structural only, without semantic review-quality automation. |
| `T10`, `T12`, `T16` | Downstream skills and generated adapters remain aligned with closeout and summary guidance. |
| `T14` | Final lifecycle validation catches stale plan state, open review-resolution, and missing review closeout. |

## Verification Evidence

Final M4 validation passed with:

- `python scripts/test-review-artifact-validator.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/changes/2026-04-24-review-finding-resolution-contract/explain-change.md --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md --path docs/workflows.md --path AGENTS.md --path CONSTITUTION.md`
- `python scripts/validate-release.py --version v0.1.1`
- `git diff --check -- .`
- `bash scripts/ci.sh`

## Review Resolution Summary

The durable review-resolution record is `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`.

Counts by disposition:

- Accepted: 7
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0

Material findings closed:

- `AR1`, `AR2`
- `SR1`, `SR2`, `SR3`
- `CR1-F1`, `CR2-F1`

This explanation links to the detailed review-resolution artifact instead of duplicating every finding and suggested solution.

## Alternatives Rejected

Extending the artifact lifecycle validator was rejected because lifecycle validation owns top-level artifact state, while this feature needs per-change review record parsing.

Extending the change metadata validator was rejected because `change.yaml` should remain a machine-readable index, not a Markdown review parser.

Requiring full review artifacts for clean reviews was rejected because the approved contract preserves lightweight clean-review behavior.

Adding semantic review-quality automation was rejected because v1 validates structure, links, IDs, dispositions, and closeout fields only.

## Scope Control

This change does not ingest maintainer PR review comments, judge whether review evidence is persuasive, require empty review artifacts for clean reviews, change runtime product behavior outside workflow policy, add third-party dependencies, or require installed Codex, Claude Code, or OpenCode for non-smoke validation.

Generated `.codex/skills/` and `dist/adapters/` outputs remain derived from canonical `skills/`.

## Risks And Follow-Ups

Remaining risk is process adoption: authors must use the canonical labels for new detailed review records. The mitigation is explicit skill guidance plus repository-owned structure and closeout validation.

No implementation blocker remains. The change is ready for final review, verification, and PR handoff.
