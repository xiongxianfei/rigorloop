# M6 Activation Evidence

Stage: implement
Milestone: M6
Result: passed

The single public activation source is `skills/workflow/SKILL.md`.
It now creates `stage-owned-change-local-v1` by default for new governed
changes and requires one migration before the first mutation of resumed
nonterminal historical work. No flag, selector, profile, capability, or
second activation source was added.

The owning change record was migrated atomically in the implementation diff:
settled artifact entries point to their peer-review evidence, M1-M5 are
closed, M6 is review-requested, the verify target is preserved, and PR or any
other external action remains outside the automation boundary.

Post-cutover validation:

- canonical skill contract suite: passed, 268 tests;
- change-metadata suite: passed, 61 tests;
- workflow-state suite: passed, 65 tests;
- current change-metadata validation: passed;
- adapter distribution: passed, 133 tests;
- broad smoke: passed, 12 checks in 352 seconds.
