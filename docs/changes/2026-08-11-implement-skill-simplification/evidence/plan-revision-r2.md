# Plan Revision Evidence R2: Implement Skill Simplification

Artifact ID: plan
Artifact path: `docs/plans/2026-08-11-implement-skill-simplification.md`
Authoring stage: plan
Completion status: complete
Resulting review request: plan-review
Date: 2026-08-11

Test-spec authoring checked the approved boundary-validation command against the current CLI and found that `validate-boundary-first.py` does not accept `--proof`. The plan now uses its supported `--check --path <feature-spec>` interface, which discovers the matching `.test.md` proof map. No milestone, requirement, proof obligation, or validation scope changed.
