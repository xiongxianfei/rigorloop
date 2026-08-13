# Spec Revision R1: Plan-Review Skill Simplification

Stage: spec
Date: 2026-08-13
Spec: `specs/plan-review-skill-simplification.md`
Trigger: `PLRSIM-ARCH-001` in `evidence/architecture-assessment-r1.md`

The revision replaces ambiguous “plan content identity” wording with the already approved identity contract: stable artifact identity is artifact ID, kind `plan`, role `primary`, and normalized path; reviewed revision identity is review ID, round, record path, reviewed artifact path, and reviewed repository revision or commit. The specification now explicitly forbids a governed-document hash or `content_identity` field.

No operation, state, authority, output, compatibility, measurement, or acceptance outcome changed. The correction restores exact agreement with `ADR-20260813-reviewed-plan-initialization-and-settlement.md` and `specs/plan-skill-simplification.md`.
