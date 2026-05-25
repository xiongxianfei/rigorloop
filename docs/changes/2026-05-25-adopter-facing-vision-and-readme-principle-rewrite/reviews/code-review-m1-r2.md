# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M1. Vision, README, and Evidence Rewrite
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/reviews/code-review-m1-r2.md`, `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/review-log.md`, `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/review-resolution.md`, `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`, `docs/plan.md`, `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: VRP-CR-M1-F2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/review-log.md`
- Review resolution: `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/review-resolution.md`
- Reviewed milestone: M1. Vision, README, and Evidence Rewrite
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1
- Required review-resolution: yes
- Finding IDs: VRP-CR-M1-F2
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface:
  - scoped M1 files: `VISION.md`, `README.md`, `docs/proposals/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`, `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`, `docs/plan.md`, `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/`, `docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md`, and `docs/learn/topics/workflow-stage-order.md`
  - branch diff against `origin/main`: `git diff --name-only origin/main...HEAD`
  - implementation commits: `303a7e0`, `1fc78d9`, `3f5c121`
- Tracked governing branch state:
  - current branch: `proposal/adopter-facing-vision-readme-principles`
  - merge base with `origin/main`: `02a9d7d6d514fc99908abf32898494dbbbae00c9`
- Governing artifacts:
  - accepted proposal `docs/proposals/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
  - active plan `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
  - review resolution `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/review-resolution.md`
  - sync proof `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/vision-readme-sync-proof.md`
  - behavior proof `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/behavior-preservation.md`
  - cold-read proof `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/cold-read-review.md`
- Validation evidence run during review:
  - `python scripts/validate-readme.py README.md --vision-markers`: passed
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`: passed
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`: passed before this review finding was recorded
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml`: passed
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path VISION.md --path README.md --path docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml --path docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md --path docs/plan.md --path docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md --path docs/learn/topics/workflow-stage-order.md`: passed
  - `git diff --check --`: passed

## Diff Summary

The scoped M1 implementation rewrites `VISION.md` and README public
positioning, adds a Mermaid workflow chain, worked-example section,
benefit-first principles, change-local sync and behavior evidence, formal
review records, a plan, a plan index entry, and learn artifacts for the
plan-before-test-spec public framing.

The published branch is not limited to the scoped M1 implementation when
compared with `origin/main`. The branch is stacked on other unmerged release,
target-native init, adapter, validator, skill, and planning work.

## Findings

### VRP-CR-M1-F2 - Published branch diff includes unrelated runtime and release surfaces

Finding ID: VRP-CR-M1-F2

- Severity: major
- Location: `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/behavior-preservation.md`; branch diff against `origin/main`
- Evidence: The behavior proof says the slice is limited to `VISION.md`, `README.md`, lifecycle evidence, plan/index files, and learn artifacts, and states that no runtime, CLI, skill, adapter, validator, release, npm package, or generated artifact behavior is changed. The active plan also marks runtime behavior, skill behavior, generated skill content, adapter output, validators, release process, and npm package behavior as non-goals. But `git diff --name-only origin/main...HEAD` for the published branch includes unrelated files such as `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/test/cli.test.js`, `scripts/adapter_distribution.py`, `scripts/skill_validation.py`, `skills/plan/SKILL.md`, `docs/releases/v0.3.0.md`, `docs/releases/v0.3.1.md`, `specs/target-native-init.md`, and `specs/installed-skill-artifact-placement-contract.md`.
- Required outcome: The branch/review surface for this initiative must match the behavior-preservation proof before M1 can close. Reviewers must not see unrelated runtime, release, validator, skill, or adapter changes as part of the adopter-facing vision/README rewrite unless those changes are explicitly outside the PR diff through the chosen base.
- Safe resolution path: Either rebase or recreate this initiative branch on a base that already contains the stacked target-native init/release/placement work, or create a clean branch from `origin/main` and cherry-pick only the adopter-facing vision/README commits and evidence. If the intended review is stacked, publish or record the intended base branch/merge order and update the behavior-preservation proof to say the no-runtime-change claim applies to the scoped M1 commits, not to a PR diff against `origin/main`.
- needs-decision rationale: none

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Scoped `VISION.md` and README copy follow the accepted benefit-first direction, but the published branch diff violates the plan non-goal that runtime, release, skill, adapter, validator, and npm surfaces stay out of this initiative. |
| Test coverage | pass | Documentation validation and lifecycle/review validators passed for the scoped artifacts. No code behavior tests are required for the scoped documentation rewrite. |
| Edge cases | concern | The plan's branch/review-surface edge case is not safe: a reviewer opening the branch against `origin/main` sees unrelated behavior-changing work. |
| Error handling | pass | Missing cold-read evidence was resolved through review-resolution, and validators now pass for the change-local review artifacts before this new finding. |
| Architecture boundaries | concern | M1 itself does not edit architecture/runtime files, but the published branch diff includes unrelated architecture, runtime, release, validator, and skill files. |
| Compatibility | concern | README command examples come from the stacked target-native init base; that is acceptable only if the review base includes that work before this branch is reviewed. |
| Security/privacy | pass | No secrets or private runtime values were observed in the scoped documentation diff. |
| Derived artifact currency | pass | `validate-readme.py README.md --vision-markers` passed, and the sync proof records marker/prose ownership. |
| Unrelated changes | block | `git diff --name-only origin/main...HEAD` lists many non-M1 files, including package runtime, tests, release records, validators, skills, and separate specs/plans. |
| Validation evidence | pass | The named validators passed for the scoped M1 artifacts; the finding is about branch review-surface scope, not failed validation. |

## No-Finding Rationale

Not applicable. The review has material finding `VRP-CR-M1-F2`.

## Direct-Proof Gaps

No direct-proof gap remains for the scoped README/VISION rewrite. The remaining
issue is that the published branch diff does not match the scoped
behavior-preservation claim.

## Milestone Handoff

- Reviewed milestone: M1. Vision, README, and Evidence Rewrite
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1
- Next stage: review-resolution
- Final closeout readiness: not ready; M1 has an open material code-review finding, and explain-change, verify, and PR handoff have not run.
