# M5 Code Review R1

Review ID: code-review-m5-r1
Stage: code-review
Round: 1
Reviewer: Codex independent contract-first code-review peer
Target: f4406555..9af50407
Reviewed artifact: commit 9af50407
Reviewed milestone: M5
Review date: 2026-08-10
Recording status: recorded
Status: changes-requested
Review status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and matching review state
- Open blockers: PSR-CR-M5-R1-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PSR-CR-M5-R1-001
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/code-review-m5-r1.md
- Review log: docs/changes/2026-08-10-published-skill-first-repository-simplification/review-log.md
- Review resolution: required before fixing
- Reviewed milestone: M5
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5, M6
- Required review-resolution: yes
- Finding IDs: PSR-CR-M5-R1-001
- Verify readiness: not-claimed

## Diff summary

The slice adds review-root association, composes review-artifact structure
validation behind the lifecycle entry point, names the public governance owner,
preserves the focused suites, and adds no new CLI, selector, cache, or scheduler.
The review parser composition and diagnostic translation are bounded and
actionable.

## Finding PSR-CR-M5-R1-001

Finding ID: PSR-CR-M5-R1-001
Severity: major
Location: `scripts/artifact_lifecycle_validation.py:1850-1907`; `scripts/validate-change-metadata.py:2160-2190`
Evidence: the public lifecycle path calls `_parse_change_yaml_text` and only
applies `validate_stage_owned_lifecycle_metadata` when the stage-owned marker is
present. It never calls the focused validator's `validate_file`, schema
validation, or full `validate_metadata_semantics`. Therefore malformed ordinary
change-record fields and closed-vocabulary values can pass the public owner even
though `python scripts/validate-change-metadata.py` rejects them.
Required outcome: The public governance entry point must apply the focused
change-metadata validator's complete file contract to every in-scope
`change.yaml`, translate every error under `change_metadata`, and preserve the
existing stage-owned and review-artifact checks without duplicating their data
models.
Safe resolution path: Reuse the already loaded focused module and its
`validate_file` API, add a public-entry regression with a focused invalid
change-metadata fixture, deduplicate any identical stage-owned errors, and rerun
all M5 commands. Do not alter metadata schemas, vocabularies, workflow routing,
cache behavior, selector behavior, or M6 surfaces.
needs-decision rationale: none
Auto fix class: declared-safe

## Checklist coverage

1. Spec alignment: block — R12 requires the one public owner to preserve shape and closed-vocabulary failures.
2. Test coverage: block — the new integration test proves review composition only, not full change-metadata composition.
3. Edge cases: block — malformed non-stage-owned metadata can bypass the public route.
4. Error handling: pass for review findings and public owner labels.
5. Architecture boundaries: concern — review composition is correct, but change-metadata remains a competing required route.
6. Compatibility: pass — focused modules and active cache/selector contracts remain intact.
7. Security/privacy: pass — local filesystem only.
8. Derived artifact currency: not applicable.
9. Unrelated changes: pass — bounded M5 diff.
10. Validation evidence: concern — 347 focused tests pass, but parity is not established at the public composition edge.

## Requirement-fidelity result

R13, R15, and R16 pass for the reviewed slice. R12 and T8 fail because the
single public result does not yet preserve the full focused change-metadata
contract.

## Milestone handoff

M5 remains `resolution-needed`; M6 remains planned. Verify is not ready.
