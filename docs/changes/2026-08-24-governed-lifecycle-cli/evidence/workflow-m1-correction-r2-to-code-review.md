# Workflow Transition: M1 Correction R2 to Code Review

- Change ID: `2026-08-24-governed-lifecycle-cli`
- Milestone: `M1`
- Corrected implementation commit: `b5d55924`
- Prior review: `code-review-m1-r2`
- Prior state: `implementing`
- Review state: `review-requested`
- Correction evidence: `evidence/m1-correction-r2.md`
- Selected stage: `code-review`
- Required independence: `L2` because the changed surface is elevated risk
- Available independence: `L0` in the current authoring context
- Automation status: `paused`
- Stop reason: `missing-review-evidence`
- Resume condition: an explicitly authorized separate review agent or independently created session records an eligible review and the required elevated-risk second review
- Automation target: singleton `verify`
- Transition owner: workflow

The workflow did not create a clean receipt or advance M1. `specs/review-independence-and-criticality.md` R1, R2, and R14c prohibit automated handoff from the available same-context review and require an elevated-risk second review.
