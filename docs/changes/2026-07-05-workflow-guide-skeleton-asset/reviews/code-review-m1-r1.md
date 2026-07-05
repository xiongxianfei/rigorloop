# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Canonical skeleton asset and workflow skill mapping
Reviewed artifact: commit 56107196
Review date: 2026-07-05
Reviewed commit: 56107196
Status: changes-requested
Review status: changes-requested
Material findings: WGS-M1-CR1, WGS-M1-CR2, WGS-M1-CR3
Recording status: recorded
Recording blocker: none
Reviewed milestone: M1
Milestone closeout: resolution-needed
Required review-resolution: yes
Immediate next stage: review-resolution M1
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m1-r1.md
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: WGS-M1-CR1, WGS-M1-CR2, WGS-M1-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-log.md
- Review resolution: docs/changes/2026-07-05-workflow-guide-skeleton-asset/review-resolution.md#code-review-m1-r1
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: WGS-M1-CR1, WGS-M1-CR2, WGS-M1-CR3
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `56107196 M1: add workflow guide skeleton asset`.
- Tracked governing branch state: accepted proposal, approved workflow-map spec amendment, active test spec, clean test-spec-review, active plan, and M1 implementation are tracked on branch `proposal/workflow-guide-skeleton-asset`.
- Governing artifacts: `specs/workflow-skill-artifact-location-map.md`, `specs/workflow-skill-artifact-location-map.test.md`, `docs/plans/2026-07-05-workflow-guide-skeleton-asset.md`, `docs/changes/2026-07-05-workflow-guide-skeleton-asset/reviews/test-spec-review-r1.md`.
- Validation evidence: M1 validation notes in `docs/plans/2026-07-05-workflow-guide-skeleton-asset.md` and `docs/changes/2026-07-05-workflow-guide-skeleton-asset/change.yaml`.

## Diff summary

M1 adds `skills/workflow/assets/workflows-skeleton.md`, maps it from `skills/workflow/SKILL.md` with a `COPY` resource-map entry, adds focused M1 tests in `scripts/test-skill-validator.py`, and updates plan and change metadata to request M1 code review.

## Findings

### WGS-M1-CR1 - Skeleton source rank omits required source authorities

Finding ID: WGS-M1-CR1
Severity: major
Location: `skills/workflow/assets/workflows-skeleton.md:23`
Evidence: The skeleton source-rank list jumps from active artifact metadata and workflow-managed change metadata directly to "This workflow guide" at lines 23-26. The approved workflow-map spec requires the workflow map source rank to include "active artifact metadata, active plan metadata, or active change metadata" and then "approved specs or schemas" before `docs/workflows.md` (R26 at `specs/workflow-skill-artifact-location-map.md:167`). Because this skeleton is copied to create `docs/workflows.md`, it would instantiate a project guide that omits active plan metadata and approved specs or schemas from the required precedence chain.
Required outcome: Update the skeleton `Source rank` section to reflect the approved source-rank order, including active plan metadata and approved specs or schemas before the workflow guide.
Safe resolution path: Revise `skills/workflow/assets/workflows-skeleton.md` source-rank text, extend the M1 test to assert the required source-rank terms, rerun `python scripts/test-skill-validator.py -k workflow_guide_skeleton_m1`, `python scripts/test-skill-validator.py -k workflow`, `python scripts/validate-skills.py`, lifecycle/change-metadata validation, prose validation, and `git diff --check`, then return M1 to code-review.
needs-decision rationale: none

### WGS-M1-CR2 - Skeleton change-plan path does not exactly match the approved canonical path

Finding ID: WGS-M1-CR2
Severity: major
Location: `skills/workflow/assets/workflows-skeleton.md:122`
Evidence: The skeleton registry and tables use `docs/plans/YYYY-MM-DD-<slug>.md` for `change_plan`. The approved workflow-map spec says the artifact registry MUST document `docs/plans/YYYY-MM-DD-slug.md` as the canonical detailed plan-body path (R17 at `specs/workflow-skill-artifact-location-map.md:149`). This matters because M2 is planned to validate skeleton registry/table alignment through the workflow-map contract, and the current skeleton bakes in a divergent path literal.
Required outcome: Make the skeleton's `change_plan` registry entry, artifact-location table row, and plan-surfaces row match the approved canonical path literal `docs/plans/YYYY-MM-DD-slug.md`.
Safe resolution path: Replace the three `docs/plans/YYYY-MM-DD-<slug>.md` skeleton occurrences with `docs/plans/YYYY-MM-DD-slug.md`, add or tighten M1 test assertions for the exact plan path, rerun the M1 validation set, and return M1 to code-review.
needs-decision rationale: none

### WGS-M1-CR3 - Stage obligations table embeds lifecycle policy instead of structural placeholders

Finding ID: WGS-M1-CR3
Severity: major
Location: `skills/workflow/assets/workflows-skeleton.md:54`
Evidence: The skeleton fills the `Stage obligations` table with concrete obligation values, required inputs, output artifacts, and downstream-blocking conditions for every lifecycle stage at lines 54-72. The approved skeleton requirement says the asset must remain structural, containing headings, tables, registry shape, placeholders, and brief fill instructions only, and MUST NOT own lifecycle stage policy or stage semantics (R59 at `specs/workflow-skill-artifact-location-map.md:237`; AC25 at `specs/workflow-skill-artifact-location-map.md:444`). A copied customer guide from this skeleton would carry lifecycle policy from the asset itself rather than from approved specs or project-local workflow guidance.
Required outcome: Convert the stage-obligations portion of the skeleton to structural scaffolding and brief fill guidance, or otherwise clearly mark stage values as project-local fill targets sourced from the approved workflow contract rather than policy owned by the asset.
Safe resolution path: Replace the fully populated stage-obligations table with a compact scaffold row or placeholder-oriented table that preserves the required section shape without enumerating lifecycle policy, add a regression assertion that the skeleton does not include the full policy table, rerun the M1 validation set, and return M1 to code-review.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | WGS-M1-CR1 and WGS-M1-CR2 show source-rank and plan-path drift from approved R26 and R17; WGS-M1-CR3 violates structural-only R59/AC25. |
| Test coverage | concern | The new tests prove asset presence, required headings, and a few forbidden phrases, but they do not prove exact source-rank terms, exact plan path, or absence of policy-filled stage-obligation rows. |
| Edge cases | concern | EC22 is not directly protected because the skeleton can include full lifecycle-obligation semantics while still passing the current forbidden-term assertions. |
| Error handling | pass | M1 is static skill/template content; no runtime error-handling path is introduced. |
| Architecture boundaries | pass | Architecture assessment recorded `architecture-not-required`; M1 stays in canonical skills, tests, and lifecycle artifacts. |
| Compatibility | concern | The skeleton does not migrate existing `docs/workflows.md`, but copied future guides could inherit source-rank and plan-path drift. |
| Security/privacy | pass | The skeleton contains repository-relative paths and no secrets, credentials, machine-local paths, or external service requirements. |
| Derived artifact currency | pass | M1 does not touch generated mirrors or adapters; M3 owns generated packaging proof. |
| Unrelated changes | pass | The diff is scoped to the workflow skill, new skeleton asset, focused tests, and lifecycle state. |
| Validation evidence | concern | Recorded validation commands are credible for the current assertions, but they miss the contract drift identified in WGS-M1-CR1 through WGS-M1-CR3. |

## Recommended next stage

`review-resolution M1` for WGS-M1-CR1, WGS-M1-CR2, and WGS-M1-CR3, followed by targeted implementation fixes on M1 and a rerun code-review.

## Milestone handoff

- Reviewed milestone: M1
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2, M3
- Next stage: review-resolution M1
- Final closeout readiness: not ready; M1 has open material findings and M2/M3 remain unimplemented.
