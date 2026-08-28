# Review independence and broad-smoke blocker

- Stage: workflow/code-review
- Milestone: M1
- Local review result: no new material implementation finding
- Automated review gate: inconclusive
- Blocking invariant: automated workflow review requires independence level L1, L2, or L3; the available direct reviewer is L0 and the user explicitly prohibited a subagent reviewer.
- Broad-smoke preflight: `bash scripts/ci.sh --mode broad-smoke --jobs 2` exited 1 only because review-artifact and artifact-lifecycle checks rejected the L0 review's attempted `advance` outcome.
- Product checks before the gate: 27 focused tests, 206 package tests, 4 measurement tests, 3 wrapper tests, 154 selector tests, the six-profile measurement gate, and focused packed-package proof passed.
- Required next action: authorize an independent reviewer or explicitly stop the workflow at this gate. Do not relabel L0 as independent.
