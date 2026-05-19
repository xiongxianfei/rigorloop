# Published Skill Design Implement And Code-Review Routing Coverage

Change: `2026-05-19-published-skill-design-implement-code-review`

These tables are deterministic review evidence. They do not claim runtime model auto-selection in CI.

## `implement`

| Prompt class | Example prompt | Expected routing | Notes |
|---|---|---|---|
| Obvious positive | "Implement M2 from the active plan and update validation notes." | Trigger `implement`. | Approved milestone implementation with plan updates and validation. |
| Casual positive | "Do the next planned implementation slice." | Trigger `implement` when an active plan/test spec identifies the slice. | Description should mention reviewed milestone and validation evidence. |
| Edge positive | "Fix accepted code-review findings for the same milestone and return it to review-requested." | Trigger `implement`. | Uses review-resolution evidence and same-milestone fix loop. |
| Near negative | "Review the implementation diff and tell me if it passes." | Do not trigger `implement`; use `code-review`. | Review rather than implementation. |
| Near negative | "Open the PR after final verify." | Do not trigger `implement`; use `pr` after verify readiness. | PR handoff is downstream. |
| Competing skill | "Reproduce and fix a bug with a regression test." | Usually `bugfix`, unless the active plan assigns a reviewed milestone. | Bugfix has a specialized bug workflow. |
| Should not trigger | "Explain what this code does." | No `implement`. | Generic explanation. |

## `code-review`

| Prompt class | Example prompt | Expected routing | Notes |
|---|---|---|---|
| Obvious positive | "Code-review M1 against the plan, spec, tests, and validation evidence." | Trigger `code-review`. | Independent implementation review. |
| Casual positive | "Review this implementation slice before we move on." | Trigger `code-review` when a diff or changed files exist. | Description should mention implementation diff/review surface. |
| Edge positive | "Rerun review after the accepted finding fix." | Trigger `code-review`. | Review-resolution evidence is conditional input. |
| Near negative | "Resolve the material finding." | Do not trigger `code-review`; use review-resolution/fix flow first. | Findings must be recorded before fixes. |
| Near negative | "Verify the branch is ready for PR." | Do not trigger `code-review`; use `verify`. | Verification/branch-ready is downstream. |
| Competing skill | "Review the plan before implementation." | Use `plan-review`, not `code-review`. | Different artifact and stage. |
| Should not trigger | "Summarize the project architecture." | No `code-review`. | Generic or architecture-specific task. |

## Coverage Notes

- Both descriptions should route from frontmatter `description`, not body-only `When to use` sections.
- Body routing sections may clarify local stop conditions and competing skills after the skill loads.
- Future transcript evidence can add under-triggering or over-triggering observations, but no transcript is required for M1 closeout.
