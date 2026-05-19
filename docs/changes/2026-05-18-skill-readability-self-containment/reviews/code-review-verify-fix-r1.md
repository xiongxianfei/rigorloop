# Code Review: Verify-Stage Adapter Compatibility Fix

Review ID: code-review-verify-fix-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: verify-stage adapter compatibility fix
Reviewed artifact: commit `b584306` (`Fix readability frontmatter adapter validation`)
Review date: 2026-05-19
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Status: complete
- Review status: changes-requested
- Material findings: SRSC-VERIFY-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-18-skill-readability-self-containment/reviews/code-review-verify-fix-r1.md
- Review log: docs/changes/2026-05-18-skill-readability-self-containment/review-log.md
- Review resolution: docs/changes/2026-05-18-skill-readability-self-containment/review-resolution.md
- Artifacts changed: review record, review log, review resolution, plan body, plan index, change metadata
- Open blockers: SRSC-VERIFY-CR1
- Next stage: review-resolution for SRSC-VERIFY-CR1, then rerun code-review
- Reviewed milestone: verify-stage adapter compatibility fix after M3 final closeout started
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: SRSC-VERIFY-CR1
- Verify readiness: not ready; verify-stage fix has an open material finding

## Review Inputs

- Diff/review surface: commit `b584306 Fix readability frontmatter adapter validation`
- Tracked governing branch state: clean local worktree on `proposal/2026-05-18-skill-readability-self-containment`
- Governing artifacts: `specs/skill-readability-contract.md`, `specs/skill-readability-contract.test.md`, `docs/plans/2026-05-18-skill-readability-self-containment.md`, `docs/plan.md`, `docs/changes/2026-05-18-skill-readability-self-containment/explain-change.md`
- Validation evidence: selected CI after verify-stage fix, broad smoke after verify-stage fix, artifact lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --` recorded in `change.yaml` and the active plan

## Diff Summary

The verify-stage fix does three things:

- treats `version` and `schema-version` as transformable front matter in `scripts/adapter_distribution.py`, preserving Codex output while dropping those fields for Claude and OpenCode generated skill bodies;
- extends adapter distribution tests and the `transformable-frontmatter` fixture to cover those two fields;
- classifies `tests/fixtures/adapters/` paths as adapter validation inputs and adds selector regression coverage.

The plan and plan index were also updated to stop at this code-review before final verify can claim branch readiness.

## Findings

### SRSC-VERIFY-CR1 - Major - `explain-change.md` still advertises stale verify readiness

Finding ID: SRSC-VERIFY-CR1
Severity: major
Location: `docs/changes/2026-05-18-skill-readability-self-containment/explain-change.md:139`, `docs/changes/2026-05-18-skill-readability-self-containment/explain-change.md:146`

Evidence: Line 139 says the next stage is `verify`; line 146 says "`explain-change` is recorded. The next lifecycle stage is `verify`." The active plan now says the next stage is `code-review` for the verify-stage adapter compatibility fix, because verify already ran, found the compatibility regression, and stopped before branch-ready.

Required outcome: Update `explain-change.md` so its readiness and risk language no longer claims the next lifecycle stage is `verify` or that final verify has simply not run. It should state that verify ran, found and fixed a compatibility issue, and the current active-plan handoff is code-review/review-resolution until the finding is resolved and verify reruns.

Safe resolution path: Reword the stale readiness/risk rows in `explain-change.md`, then rerun artifact lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --`.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | The adapter fix supports R35 by letting existing non-Codex consumers ignore `version` and `schema-version`; it does not change adapter package format or release archive contracts. |
| Test coverage | pass | `test_adapter_generation_drops_transformed_frontmatter_for_non_codex`, `test_argument_hint_is_explicit_transform_not_exclusion`, and selector fixture routing tests cover the changed behavior. |
| Edge cases | pass | The non-Codex generated output path is explicitly tested to omit `argument-hint`, `schema-version`, and `version`, while Codex output keeps them. |
| Error handling | pass | Selector now classifies adapter fixture paths instead of producing an unclassified-path block. |
| Architecture boundaries | pass | The change stays in adapter distribution and validation selection logic; generated adapter bodies are not hand-edited. |
| Compatibility | pass | The compatibility issue detected by verify is fixed in adapter transformation, preserving portability for `proposal` and `proposal-review`. |
| Security/privacy | pass | No secrets, credentials, or unsafe logging changes are present in the reviewed diff. |
| Derived artifact currency | pass | Selected CI and broad smoke include generated skill and adapter checks; no tracked generated adapter body was edited. |
| Unrelated changes | concern | `explain-change.md` was touched by the verify-stage fix but still contains stale lifecycle readiness text. |
| Validation evidence | pass | Selected CI and broad smoke passed after the fix; broad smoke's token-cost message is documented as matching `origin/main` and non-fatal. |

## No-finding rationale

Not applicable. One material finding remains.

## Recommended next stage

`review-resolution` for SRSC-VERIFY-CR1, then rerun `code-review` for the verify-stage fix.

## Handoff summary

- Reviewed milestone: verify-stage adapter compatibility fix after M3 final closeout started
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: SRSC-VERIFY-CR1
- Remaining in-scope implementation milestones: none
- Next stage: review-resolution
- Final closeout readiness: blocked until SRSC-VERIFY-CR1 is resolved and code-review reruns cleanly
