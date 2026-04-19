---
name: verify-change
description: Verify a code or documentation change using the repository's actual checks. Use when the user asks to validate work, check whether a branch is ready, or confirm the smallest credible verification set for a scoped change.
---

Follow this workflow:

1. Read `AGENTS.md` and inspect existing scripts, task runners, and `.github/workflows`.
2. Choose the smallest relevant checks for the changed files.
3. Run narrow checks first, then broader checks only when needed.
4. Stop on the first failure and report it clearly.
5. In the final report, list:
   - commands actually run
   - result of each command
   - any checks intentionally not run
   - residual risk

Do not claim full verification if only partial checks were run.
