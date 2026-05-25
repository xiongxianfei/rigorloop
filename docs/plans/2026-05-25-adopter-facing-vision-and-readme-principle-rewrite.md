# Adopter-Facing Vision and README Principle Rewrite Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Start date: 2026-05-25
- Last updated: 2026-05-25
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the accepted adopter-facing vision and README rewrite so RigorLoop's
public story leads with adopter value: AI-assisted work that remains traceable,
resumable, and reviewable after the chat ends. The implementation must preserve
`VISION.md` as the durable source of truth, keep README marker-owned content
separate from landing-page prose, avoid command-contract changes, and prove that
no runtime, skill, adapter, validator, release, or generated-output behavior
changed.

## Source artifacts

- Proposal: [Adopter-Facing Vision and README Principle Rewrite](../proposals/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md)
- Spec: not-required; existing [Vision Skill](../../specs/vision-skill.md) covers README marker ownership and synchronization boundaries.
- Architecture: not-required; this is a documentation and source-of-truth wording change within existing `VISION.md` / README boundaries.
- Test spec: not-required for the first slice; the accepted proposal provides VRP and AC checks, and the plan maps them to validation evidence.
- Change metadata: [change.yaml](../changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml)
- Review evidence: [proposal-review-r1](../changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/reviews/proposal-review-r1.md)

## Context and orientation

The current README already has one valid `<!-- vision:start -->` /
`<!-- vision:end -->` marker block near the top of the file. The marker-sync
contract is existing scope, not new tooling: `specs/vision-skill.md` `R40`-`R48`
define marker shape, generated front-matter contents, marker insertion limits,
inside-marker replacement, malformed-marker blocking, and the rule that the
vision skill must not edit README content outside the marker block except for
allowed marker insertion.

Implementation therefore has two README surfaces:

- marker-owned README front-matter generated from `VISION.md`;
- ordinary README landing-page prose outside the marker, constrained by
  `VISION.md` but not generated from it.

The accepted proposal also explicitly excludes CLI command changes. The README
may point users to the Quick Start, but exact command examples should remain
unchanged unless implementation records command-source proof against the current
approved CLI contract and package docs.

## Non-goals

- Do not redefine workflow semantics or lifecycle stage order.
- Do not change CLI command contracts or independently rewrite Quick Start
  command examples.
- Do not change runtime behavior, skill behavior, generated skill content,
  adapter output, validators, release process, or npm package behavior.
- Do not add README generation tooling or a required README synchronization
  helper script.
- Do not fabricate a synthetic worked example.
- Do not expand this slice into GitHub metadata, npm metadata, screenshots,
  GIFs, docs-site work, or launch posts.

## Requirements covered

- VRP-001, VRP-002, AC-VRP-001, AC-VRP-002: M1 updates `VISION.md` to lead with the adopter problem and durable value proposition.
- VRP-003, AC-VRP-003, AC-VRP-010: M1 reframes the five principles as adopter benefits, including learn as reliability.
- VRP-004, AC-VRP-004: M1 rewrites README first-screen positioning without changing command contracts.
- VRP-005, VRP-019, AC-VRP-005, AC-VRP-019: M1 includes a Mermaid traceability visual with required caption.
- VRP-006, AC-VRP-006: M1 places detailed mechanism/principle copy below hook, Quick Start, and visual.
- VRP-007, VRP-020, AC-VRP-020: M1 links a public-friendly real worked example or records a scheduled follow-up with owner, trigger, and candidate criteria.
- VRP-008, AC-VRP-007: M1 preserves when-to-use and when-not-to-use guidance.
- VRP-009, VRP-013, VRP-014, VRP-015, AC-VRP-008, AC-VRP-013, AC-VRP-014, AC-VRP-015: M1 records `vision-readme-sync-proof.md`.
- VRP-010, VRP-017, AC-VRP-009, AC-VRP-017: M1 records cold-read evidence from a genuinely unfamiliar reviewer.
- VRP-011, VRP-016, VRP-018, AC-VRP-011, AC-VRP-016, AC-VRP-018: M1 avoids unsupported claims and exact command changes unless command-source proof is recorded.
- VRP-012, AC-VRP-012: M1 records `behavior-preservation.md` and validation proves runtime, skill, adapter, validator, release, and generated-output surfaces are untouched.

## Current Handoff Summary

- Current milestone: M1. Vision, README, and Evidence Rewrite
- Current milestone state: resolution-needed
- Last reviewed milestone: M1. Vision, README, and Evidence Rewrite
- Review status: code-review-m1-r1 blocked on missing cold-read evidence
- Remaining in-scope implementation milestones: M1
- Next stage: review-resolution / complete M1 cold-read evidence, then return to code-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: code-review-m1-r1 recorded blocker `VRP-CR-M1-F1`; cold-read evidence is not complete, M1 is not cleanly reviewed or closed, and explain-change, verify, and PR handoff have not run.

## Milestones

### M1. Vision, README, and Evidence Rewrite

- Milestone state: resolution-needed
- Goal: Rewrite `VISION.md` and README public positioning while recording proof that README marker ownership, command-source boundaries, cold-read comprehension, worked-example handling, and behavior preservation are satisfied.
- Requirements: all VRP and AC checks listed in `Requirements covered`.
- Files/components likely touched:
  - `VISION.md`
  - `README.md`
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml`
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/vision-readme-sync-proof.md`
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/cold-read-review.md`
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/behavior-preservation.md`
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/explain-change.md` after code-review closeout
  - this plan and `docs/plan.md` for lifecycle state updates
- Dependencies:
  - Plan-review approval.
  - A genuinely cold reader must be available for cold-read evidence. The reviewer must not have seen this proposal or discussion.
  - If exact README command examples are changed, command-source proof must identify the governing CLI/package source and validation.
- Tests and proof to add/update:
  - `vision-readme-sync-proof.md` comparing `VISION.md`, README marker content, and README landing-page prose.
  - `cold-read-review.md` answering the proposal's cold-read questions and identifying whether the first action is command-neutral or Quick Start-oriented.
  - `behavior-preservation.md` showing no runtime, skill, adapter, validator, release, or generated-output files changed.
  - Manual worked-example selection proof, or scheduled follow-up with owner, trigger, and candidate criteria.
- Implementation steps:
  - Confirm README contains exactly one valid marker pair before editing marker-owned content.
  - Update `VISION.md` with adopter problem, durable value proposition, benefit-first principles, and boundary language.
  - Update README marker-owned front-matter from `VISION.md` without hand-editing generated marker content outside the synchronization contract.
  - Update README landing-page prose outside the marker with hook, short problem explanation, Mermaid traceability visual and required caption, worked-example link or scheduled follow-up, when-to-use guidance, and benefit-first principles.
  - Avoid changing exact Quick Start command examples unless command-source proof is recorded.
  - Create the sync proof, cold-read review, and behavior-preservation proof.
  - Update change metadata, progress, validation notes, and plan state before handing off to code-review.
- Validation commands:
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path VISION.md --path README.md --path docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml --path docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`
  - `git diff --check --`
- Expected observable result: a cold reader can state what RigorLoop is, who it is for, why traceability matters, where to start, and that learn means reliability improvement rather than project churn.
- Commit message: `M1: rewrite adopter-facing vision and README`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log updated if new decisions appear
  - surprises/discoveries updated
  - validation notes updated
  - change metadata updated
  - hand off to code-review for M1
  - material review findings resolved or explicitly dispositioned before downstream closeout
- Risks:
  - README marker content and landing-page prose are accidentally mixed.
  - The Mermaid diagram implies mandatory full lifecycle use for every task.
  - The worked-example follow-up becomes open-ended.
  - Cold-read evidence is invalid because the reviewer is not genuinely cold.
  - Quick Start command text drifts into this slice without command-source proof.
- Rollback/recovery:
  - Revert or narrow README landing-page prose while preserving marker boundaries.
  - Re-run README marker validation after any `VISION.md` or marker-block update.
  - Use command-neutral wording and link to Quick Start instead of changing command examples.
  - Record a scheduled worked-example follow-up instead of linking a confusing or fabricated example.
  - Stop downstream handoff if cold-read evidence cannot be collected honestly.

## Validation plan

- `python scripts/validate-readme.py README.md --vision-markers`: prove README marker shape and marker-boundary handling.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path VISION.md --path README.md --path docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml --path docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md --path docs/plan.md`: validate touched lifecycle-managed surfaces.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml`: validate change metadata after evidence files are added.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`: preserve proposal-review recording validity.
- `git diff --check --`: patch hygiene.
- Manual sync proof: `vision-readme-sync-proof.md`.
- Manual cold-read proof: `cold-read-review.md`.
- Manual behavior-preservation proof: `behavior-preservation.md`.

## Risks and recovery

- Risk: The rewrite becomes more attractive but less accurate.
  - Recovery: Use `VISION.md`, proposal AC checks, and behavior-preservation proof as hard constraints; revert unsupported claims.
- Risk: README marker-owned content is hand-edited outside the existing sync contract.
  - Recovery: Stop, restore marker boundaries, and re-run `python scripts/validate-readme.py README.md --vision-markers`.
- Risk: README first screen implies the full lifecycle is mandatory for every task.
  - Recovery: Keep the required Mermaid caption and preserve isolated-skill language.
- Risk: Worked-example deferral becomes permanent.
  - Recovery: If no example is linked, record owner, trigger, candidate criteria, and follow-up surface before milestone handoff.
- Risk: Cold-read evidence is biased by prior context.
  - Recovery: Choose a reviewer who has not seen the proposal or discussion; otherwise record the evidence gap and stop downstream handoff.
- Risk: Command examples become stale or conflict with target-native init work.
  - Recovery: Do not change exact commands unless command-source proof is recorded; use command-neutral first-action wording.

## Dependencies

- Accepted proposal and clean proposal-review record are in place.
- Existing README marker sync contract is available in `specs/vision-skill.md` `R40`-`R48`.
- `README.md` currently contains a valid marker block.
- Cold-read review requires a genuinely unfamiliar reviewer.
- Command-source proof is conditional and required only if exact README command examples are changed.

## Progress

- 2026-05-25: plan created from accepted proposal and clean proposal-review record.
- 2026-05-25: maintainer rejected `VRP-PLAN1` and confirmed no separate spec or test spec is needed for this documentation/source-of-truth rewrite; plan-review-r2 approved, and M1 moved to implementing.
- 2026-05-25: rewrote `VISION.md` and README adopter-facing positioning, added sync proof, behavior-preservation proof, and cold-read evidence placeholder; M1 remains blocked pending a genuinely unfamiliar cold-read reviewer.
- 2026-05-25: corrected the public traceability chain to match repository workflow order: spec, plan, then test spec.
- 2026-05-25: code-review-m1-r1 blocked M1 on missing cold-read evidence; M1 moved to resolution-needed.
- 2026-05-25: recorded maintainer-provided public-repository cold-read-style answer as supplemental evidence; it does not close the blocker because it was explicitly not from a separate unfamiliar human reviewer and did not review this branch draft.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-25 | Use one implementation milestone for the first slice. | The work is a tightly scoped documentation/source-of-truth rewrite with shared evidence artifacts; splitting marker and prose edits would create unnecessary sync churn. | Separate implementation milestones for `VISION.md`, README prose, and evidence artifacts. |
| 2026-05-25 | Treat README marker sync as existing scope. | `README.md` already has one valid marker block and `specs/vision-skill.md` `R40`-`R48` already govern marker synchronization. | Add new marker sync tooling or a new spec amendment. |
| 2026-05-25 | Keep exact command changes out of M1 unless command-source proof is recorded. | The accepted proposal explicitly excludes CLI command contract changes and target-native init work owns command shape. | Independently rewrite README command examples in this initiative. |
| 2026-05-25 | Do not add a separate test spec. | Maintainer owner decision says this documentation/source-of-truth rewrite does not need a separate spec; proof remains in accepted proposal checks and change-local evidence artifacts. | Add a focused test spec before implementation. |

## Surprises and discoveries

- `README.md` already contains one valid marker block near the top of the file.
- `specs/vision-skill.md` already defines the marker sync contract; no new marker-sync mechanism is needed for this plan.
- A genuinely unfamiliar cold-read reviewer is not available inside this thread; the implementation records that blocker instead of fabricating evidence.
- Review feedback caught an ordering error in the public traceability chain; README and `VISION.md` now show plan before test spec.

## Validation notes

- 2026-05-25: `README.md` marker presence and `specs/vision-skill.md` `R40`-`R48` inspected during planning.
- 2026-05-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md --path docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml --path docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md --path docs/plan.md` passed.
- 2026-05-25: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml` passed.
- 2026-05-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite` passed.
- 2026-05-25: `python scripts/validate-readme.py README.md --vision-markers` passed.
- 2026-05-25: `git diff --check --` passed.
- 2026-05-25: `python scripts/validate-readme.py README.md --vision-markers` passed after M1 content rewrite.
- 2026-05-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite` passed after owner-decision and M1 content updates.
- 2026-05-25: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml` passed after owner-decision and M1 content updates.
- 2026-05-25: `git diff --check --` passed after M1 content rewrite.

## Outcome and retrospective

- Pending downstream implementation, review, explain-change, verify, PR handoff, hosted CI, and human review.

## Readiness

- See `Current Handoff Summary`.
- M1 is in resolution-needed after code-review-m1-r1. Complete genuine cold-read evidence, update validation and plan state, then return M1 to code-review. Readiness is not Done; code-review closeout, explain-change, verify, and PR handoff remain.
