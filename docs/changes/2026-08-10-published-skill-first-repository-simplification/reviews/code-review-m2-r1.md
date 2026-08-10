# M2 Code Review R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex independent contract-first code-review peer
Target: 989f9aee..c845a3bf
Reviewed artifact: commit c845a3bf
Reviewed milestone: M2
Review date: 2026-08-10
Recording status: recorded
Status: changes-requested
Review status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: PSR-CR-M2-R1-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PSR-CR-M2-R1-001
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-08-10-published-skill-first-repository-simplification/review-log.md
- Review resolution: required before fixing
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: PSR-CR-M2-R1-001
- Verify readiness: not-claimed

## Diff summary

The slice names the existing canonical validator as Gate A, proves ambiguous
but structurally valid prose passes, adds static runtime-exclusion coverage,
and adds the R11 semantic checklist to code-review. Existing deterministic and
generated-projection suites pass.

## Finding PSR-CR-M2-R1-001

Finding ID: PSR-CR-M2-R1-001
Severity: minor
Location: `scripts/skill_validation.py:3499-3515`; `scripts/validate-skills.py:39-41`
Evidence: `python scripts/validate-skills.py tests/fixtures/skills/unsafe-resource-path`
on a nonexistent target enters `Path.rglob`, later calls `directory.iterdir()`,
and emits a traceback ending in `FileNotFoundError`. Gate A therefore bypasses
its stable owner prefix and provides no actionable missing-input repair.
Required outcome: A missing or unsupported Gate A target must return nonzero
through `ValidationResult`, name Gate A, name the target, and avoid a traceback.
Safe resolution path: Add an early target-existence check to the shared
`validate_skill_tree` owner and a CLI-level regression test; do not change
skill semantics, resource validation, generated output, or other gates.
needs-decision rationale: none
Auto fix class: mechanical

## Checklist coverage

1. Spec alignment: concern — the intended ownership boundaries hold, but the missing-input recovery path is not actionable.
2. Test coverage: concern — R2 fixtures are broad, but missing target is absent.
3. Edge cases: block — missing target produces a traceback.
4. Error handling: block — public Gate A result contract is bypassed.
5. Architecture boundaries: pass — one entry point and existing shared owner.
6. Compatibility: pass — existing fixture assertions tolerate the stable prefix.
7. Security/privacy: pass — local filesystem only.
8. Derived artifact currency: pass — temporary build projection passes.
9. Unrelated changes: pass — bounded M2 diff.
10. Validation evidence: pass for selected commands, but the direct missing-input probe exposes a gap.

## Requirement-fidelity result

Applicable with one failure-recovery gap. R2/R3/R11 properties otherwise map
to direct fixture or MP1 evidence.

## Milestone handoff

M2 remains `resolution-needed`; M3-M6 remain planned. Verify is not ready.
